
def heuristic(input_data):
    """FJSSP heuristic: Min makespan + load balance, local search."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    scheduled_operations = set()

    while available_operations:
        best_operation = None
        best_machine = None
        earliest_start_time = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]
            
            # Prioritize machines with lower load for initial scheduling
            sorted_machines = sorted(range(len(machines)), key=lambda i: machine_load[machines[i]])

            for machine_idx_sorted in sorted_machines:
                machine_idx = sorted_machines[machine_idx_sorted]
                machine = machines[machine_idx]
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)

        job_id, op_idx = best_operation
        machine, processing_time = best_machine

        start_time = max(machine_available_time[machine], job_completion_time[job_id])
        end_time = start_time + processing_time
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[machine] = end_time
        job_completion_time[job_id] = end_time
        machine_load[machine] += processing_time # update machine load
        available_operations.remove((job_id, op_idx))

        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))

    # Local Search: Machine reassignment to balance load
    for _ in range(5): # Iterate a few times for improvement
        for job_id in range(1, n_jobs + 1):
            for op_idx in range(len(schedule[job_id])):
                original_machine = schedule[job_id][op_idx]['Assigned Machine']
                original_start_time = schedule[job_id][op_idx]['Start Time']
                original_end_time = schedule[job_id][op_idx]['End Time']
                original_processing_time = schedule[job_id][op_idx]['Processing Time']
                
                current_operation = jobs[job_id][op_idx]
                possible_machines = current_operation[0]
                possible_times = current_operation[1]
                
                best_new_machine = original_machine
                best_makespan = float('inf')
                
                for new_machine_index, new_machine in enumerate(possible_machines):
                    new_processing_time = possible_times[new_machine_index]
                    
                    new_start_time = max(machine_available_time[new_machine] - original_processing_time if machine_available_time[new_machine] > original_processing_time else 0, job_completion_time[job_id] - original_processing_time if job_completion_time[job_id] > original_processing_time else 0)
                    new_end_time = new_start_time + new_processing_time
                                        
                    temp_schedule = {}
                    machine_available_time_temp = {m: machine_available_time[m] for m in range(n_machines)}
                    job_completion_time_temp = {j: job_completion_time[j] for j in range(1, n_jobs + 1)}
                    temp_schedule[job_id] = schedule[job_id].copy()

                    temp_schedule[job_id][op_idx]['Assigned Machine'] = new_machine
                    temp_schedule[job_id][op_idx]['Start Time'] = new_start_time
                    temp_schedule[job_id][op_idx]['End Time'] = new_end_time
                    temp_schedule[job_id][op_idx]['Processing Time'] = new_processing_time

                    machine_available_time_temp[original_machine] -= original_processing_time
                    machine_available_time_temp[new_machine] = new_end_time
                    
                    job_completion_time_temp[job_id] = new_end_time
                    
                    makespan = max(machine_available_time_temp.values())
                    
                    if makespan < best_makespan:
                        best_makespan = makespan
                        best_new_machine = new_machine
                        best_new_start_time = new_start_time
                        best_new_end_time = new_end_time
                        best_new_processing_time = new_processing_time

                if best_new_machine != original_machine:
                    machine_load[original_machine] -= original_processing_time
                    machine_load[best_new_machine] += best_new_processing_time
                    
                    schedule[job_id][op_idx]['Assigned Machine'] = best_new_machine
                    schedule[job_id][op_idx]['Start Time'] = best_new_start_time
                    schedule[job_id][op_idx]['End Time'] = best_new_end_time
                    schedule[job_id][op_idx]['Processing Time'] = best_new_processing_time
                    
                    machine_available_time[original_machine] -= original_processing_time
                    machine_available_time[best_new_machine] = best_new_end_time
    return schedule
