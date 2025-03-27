
def heuristic(input_data):
    """
    A heuristic for the FJSSP that considers machine idle time and operation processing time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    # Prioritize operations based on shortest processing time (SPT)
    operation_queue = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            operation_queue.append((job_id, op_idx, machines, times))

    # Sort the operations based on shortest processing time
    operation_queue.sort(key=lambda x: min(x[3]))

    while operation_queue:
        job_id, op_idx, machines, times = operation_queue.pop(0)
        op_num = op_idx + 1

        # Find the best machine based on earliest available time
        best_machine = -1
        min_start_time = float('inf')
        processing_time = -1

        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])

            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                processing_time = time

        # Schedule the operation on the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
