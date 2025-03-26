
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes jobs with fewer operations
    and assigns operations to machines with the earliest available time,
    aiming to balance load and reduce makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data}
    schedule = {}
    
    # Sort jobs based on the number of operations (shortest job first)
    job_priority = sorted(jobs_data.keys(), key=lambda job: len(jobs_data[job]))

    for job in job_priority:
        schedule[job] = []
        current_time = 0
        
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1
            
            # Find the machine with the earliest available time among feasible machines
            best_machine, best_time = None, float('inf')
            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                available_time = max(machine_available_time[machine], current_time)
                
                if available_time < best_time:
                    best_time = available_time
                    best_machine = machine
                    best_processing_time = time

            # Assign the operation to the best machine
            start_time = best_time
            end_time = start_time + best_processing_time
            
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })
            
            # Update machine and job completion times
            machine_available_time[best_machine] = end_time
            current_time = end_time

    return schedule
