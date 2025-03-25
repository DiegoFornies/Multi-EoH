
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes minimizing machine idle time
    and job waiting time by selecting machines based on earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize machine available times
    machine_available_time = {m: 0 for m in range(n_machines)}

    # Initialize job completion times
    job_completion_time = {j: 0 for j in jobs_data}

    schedule = {}  # Store the final schedule

    # Iterate through each job and its operations
    for job_id in jobs_data:
        schedule[job_id] = []
        job_operations = jobs_data[job_id]
        
        for op_idx, operation in enumerate(job_operations):
            machines, times = operation
            op_num = op_idx + 1  # Operation number

            # Find the machine with the earliest available time among feasible machines
            best_machine = None
            min_start_time = float('inf')
            
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_time = processing_time
            
            # Assign the operation to the best machine
            start_time = min_start_time
            end_time = start_time + best_time
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            # Update machine and job completion times
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            
    return schedule
