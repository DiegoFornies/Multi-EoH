
def heuristic(input_data):
    """Schedules jobs to minimize makespan, improve separation, and balance machine load.
    Uses a SPT-based priority and iterative refinement to optimize the schedule."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs.items()}

    # Prioritize jobs with shortest processing time operations first
    def calculate_operation_time(job, operation_index):
        machines, times = jobs[job][operation_index]
        return min(times)  # Shortest Processing Time for the operation

    job_priority = sorted(jobs.keys(), key=lambda job: calculate_operation_time(job, remaining_operations[job][0]-1) if remaining_operations[job] else float('inf'))
    
    while any(remaining_operations[job] for job in jobs):
        for job in job_priority:
            if not remaining_operations[job]:
                continue

            operation_number = remaining_operations[job][0]
            operation_index = operation_number - 1
            machines, times = jobs[job][operation_index]

            # Find the machine that allows the earliest completion time
            best_machine, best_start_time, best_end_time, best_processing_time = None, float('inf'), float('inf'), None
            
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_end_time[job])
                end_time = start_time + processing_time

                if end_time < best_end_time:
                    best_machine, best_start_time, best_end_time, best_processing_time = machine, start_time, end_time, processing_time
            
            if job not in schedule:
                schedule[job] = []

            schedule[job].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_end_time,
                'Processing Time': best_processing_time
            })
            
            machine_available_time[best_machine] = best_end_time
            job_end_time[job] = best_end_time
            remaining_operations[job].pop(0)

    # Iterative refinement (simple swap heuristic to improve balance)
    for _ in range(5): # Iterate a few times
        for job1 in schedule:
            for job2 in schedule:
                if job1 == job2:
                    continue
                for i in range(len(schedule[job1])):
                    for j in range(len(schedule[job2])):
                        machine1 = schedule[job1][i]['Assigned Machine']
                        machine2 = schedule[job2][j]['Assigned Machine']
                        
                        # Try swapping machines
                        original_makespan = max(machine_available_time.values())
                        
                        # Temporarily swap machines
                        schedule[job1][i]['Assigned Machine'] , schedule[job2][j]['Assigned Machine'] = schedule[job2][j]['Assigned Machine'], schedule[job1][i]['Assigned Machine']
                        
                        # Recalculate times for swapped operations
                        # Only consider impact on affected machines
                        
                        # Quickly recompute machine_available_time for modified machines
                        affected_machines = {machine1, machine2}
                        new_machine_available_time = {m: 0 for m in range(n_machines)}
                        new_job_end_time = {j: 0 for j in range(1, n_jobs + 1)}
                        
                        temp_schedule = {}
                        
                        all_ops = []
                        for job_num in schedule:
                            for op in schedule[job_num]:
                                all_ops.append((job_num, op))
                                
                        all_ops.sort(key = lambda x: x[1]['Start Time'])
                        
                        for job_num, op in all_ops:
                            machine = op['Assigned Machine']
                            start_time = max(new_machine_available_time[machine], new_job_end_time[job_num])
                            end_time = start_time + op['Processing Time']
                            
                            op['Start Time'] = start_time
                            op['End Time'] = end_time
                            
                            new_machine_available_time[machine] = end_time
                            new_job_end_time[job_num] = end_time
        
                        new_makespan = max(new_machine_available_time.values())
                        
                        # Accept change if it improves makespan, otherwise revert
                        if new_makespan < original_makespan:
                           machine_available_time = new_machine_available_time
                        else:
                           # Revert machine swap
                           schedule[job1][i]['Assigned Machine'] , schedule[job2][j]['Assigned Machine'] = schedule[job2][j]['Assigned Machine'], schedule[job1][i]['Assigned Machine']

    return schedule
