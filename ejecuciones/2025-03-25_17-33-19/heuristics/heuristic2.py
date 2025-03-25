
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) that considers
    machine load and job completion time to prioritize operations.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}  # Track machine load
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Track job completion
    machine_availability = {m: 0 for m in range(n_machines)} # track machine availability
    job_operations_done = {j: 0 for j in range(1, n_jobs + 1)}

    schedule = {}
    for job in jobs_data:
        schedule[job] = []

    # Initialize a list of operations to schedule
    operations_to_schedule = []
    for job in jobs_data:
        operations_to_schedule.append((job, 0)) # (job, op_index)

    scheduled_operations = set()

    while operations_to_schedule:
        # Prioritize operations based on machine load, job completion time, and shortest process time
        best_operation = None
        best_priority = float('inf')

        for job, op_index in operations_to_schedule:
            machines, times = jobs_data[job][op_index]
            op_num = op_index+1

            # Calculate priority
            for i, machine in enumerate(machines):
                processing_time = times[i]
                priority = (
                    machine_load[machine] +
                    job_completion_time[job] +
                    processing_time
                )
                if priority < best_priority:
                    best_priority = priority
                    best_operation = (job, op_index, machine, processing_time)

        # If no suitable operation is found, try to find next op in the queue
        if best_operation is None:
             break # Exit if stuck

        job, op_index, assigned_machine, processing_time = best_operation
        op_num = op_index+1

        # Schedule the operation
        start_time = max(machine_availability[assigned_machine], job_completion_time[job])
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine load and job completion time
        machine_load[assigned_machine] += processing_time
        machine_availability[assigned_machine] = end_time
        job_completion_time[job] = end_time
        job_operations_done[job] += 1

        #Remove this operation from operations_to_schedule
        operations_to_schedule.remove((job, op_index))

        # Add the next operation of the job to the list
        if op_index + 1 < len(jobs_data[job]):
            operations_to_schedule.append((job, op_index + 1))

    return schedule
