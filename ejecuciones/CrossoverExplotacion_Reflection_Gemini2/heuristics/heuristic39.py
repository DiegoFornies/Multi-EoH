
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem.
    Prioritizes operations with the shortest processing time, machine availability, and job sequence.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    operation_queue = []

    # Initialize the operation queue with the first operation of each job
    for job_id, operations in jobs.items():
        if operations:
            machines, times = operations[0]
            operation_queue.append((job_id, 0, machines, times))  # (job_id, op_idx, machines, times)

    # Sort the operation queue by shortest processing time
    operation_queue.sort(key=lambda x: min(x[3]))

    while operation_queue:
        # Select the operation with the shortest processing time
        job_id, op_idx, machines, times = operation_queue.pop(0)
        op_num = op_idx + 1

        # Find the earliest available machine for the operation
        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], job_last_end_time[job_id])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the selected machine
        start_time = best_start_time
        end_time = start_time + best_processing_time
        machine = best_machine

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine available time and job last end time
        machine_available_time[machine] = end_time
        job_last_end_time[job_id] = end_time

        # Add the next operation of the job to the queue
        if op_idx + 1 < len(jobs[job_id]):
            next_machines, next_times = jobs[job_id][op_idx + 1]
            operation_queue.append((job_id, op_idx + 1, next_machines, next_times))
            operation_queue.sort(key=lambda x: min(x[3]))  # Maintain sorted queue

    return schedule
