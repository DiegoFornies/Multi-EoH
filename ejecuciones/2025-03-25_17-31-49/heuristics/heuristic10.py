
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes shortest processing time and earliest machine availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Initialize job completion times
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    
    eligible_operations = []
    for job_id, operations in jobs.items():
        eligible_operations.append((job_id, 0)) # (job_id, operation_index)
    
    completed_operations = set() #track completed operations to avoid repeats in logic

    while eligible_operations:
        # Find the operation with the shortest possible processing time among all available operations
        best_op = None
        min_end_time = float('inf')

        for job_id, op_idx in eligible_operations:
            if (job_id, op_idx) in completed_operations:
                continue #check the dictionary for operations that have already been scheduled.

            machines, times = jobs[job_id][op_idx]

            # Find the machine with the earliest available time for this operation
            best_machine = None
            best_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])  # Consider machine and job dependencies
                end_time = start_time + processing_time

                if end_time < best_time:
                    best_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            if best_machine is not None and best_time < min_end_time:
                min_end_time = best_time
                best_op = (job_id, op_idx, best_machine, best_start_time, best_processing_time)
        
        # Schedule the best operation
        if best_op:
            job_id, op_idx, machine, start_time, processing_time = best_op
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine and job completion times
            machine_available_time[machine] = end_time
            job_completion_time[job_id] = end_time

            completed_operations.add((job_id, op_idx)) #track to ensure a given operation is only ever scheduled one time.

            # Add the next operation for this job to the eligible operations, if it exists
            if op_idx + 1 < len(jobs[job_id]):
                eligible_operations.append((job_id, op_idx + 1))

        else:
            break # Break when no best operation can be found

        #remove any operations that have already been scheduled from eligibility
        eligible_operations = [op for op in eligible_operations if op not in completed_operations]
            
    return schedule
