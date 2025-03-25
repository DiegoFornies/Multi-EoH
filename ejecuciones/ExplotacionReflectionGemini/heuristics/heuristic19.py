
def heuristic(input_data):
    """
    A heuristic for FJSSP scheduling.  Prioritizes jobs with fewer remaining operations
    and machines with lower utilization to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in jobs_data}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data}
    remaining_operations = {job: 0 for job in jobs_data}

    # Initialize remaining operations count for each job
    for job in jobs_data:
        remaining_operations[job] = len(jobs_data[job])
    
    # Create a list of operations, sorted by job number and operation index
    operations = []
    for job_id in jobs_data:
        for op_idx, op_data in enumerate(jobs_data[job_id]):
            operations.append((job_id, op_idx, op_data))

    scheduled_operations = set() # Track scheduled operations (job_id, op_idx)

    while any(remaining_operations[job] > 0 for job in jobs_data):
        # Choose the next operation based on a priority
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
            if remaining_operations[job_id] > 0 and (job_id, op_idx) not in scheduled_operations:
                is_next_operation = True
                # Check sequence feasibility
                for prev_op_idx in range(op_idx):
                    if (job_id, prev_op_idx) not in scheduled_operations:
                        is_next_operation = False
                        break

                if is_next_operation:
                    eligible_operations.append((job_id, op_idx, op_data))

        if not eligible_operations:
            break # No eligible operations, possibly due to errors in the input

        # Prioritize jobs with fewer remaining operations, then shortest processing time on least utilized machine
        best_operation = None
        min_remaining = float('inf')
        min_makespan = float('inf')

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data
            remaining = remaining_operations[job_id]
            
            # Find best machine
            best_machine = -1
            best_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]

                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + time

                if end_time < best_time:
                    best_time = end_time
                    best_machine = machine

            if remaining < min_remaining:
                min_remaining = remaining
                min_makespan = best_time
                best_operation = (job_id, op_idx, op_data, best_machine, best_time-time)
            elif remaining == min_remaining and best_time < min_makespan:
                min_makespan = best_time
                best_operation = (job_id, op_idx, op_data, best_machine, best_time-time)

        # Schedule the best operation
        job_id, op_idx, op_data, machine, start_time = best_operation
        machines, times = op_data
        time = next(t for i, t in enumerate(times) if machines[i] == machine)
        end_time = start_time + time
        op_num = op_idx + 1
        schedule[job_id].append({'Operation': op_num, 'Assigned Machine': machine, 'Start Time': start_time, 'End Time': end_time, 'Processing Time': time})
        
        # Update machine and job completion times
        machine_available_time[machine] = end_time
        job_completion_time[job_id] = end_time
        remaining_operations[job_id] -= 1
        scheduled_operations.add((job_id, op_idx))

    return schedule
