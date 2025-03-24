
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP)
    that prioritizes operations with shorter processing times and earlier due dates.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize machine availability times and job completion times.
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Flatten operations for scheduling.
    operations = []
    for job_id, operations_data in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_data):
            operations.append({
                'job_id': job_id,
                'operation_number': op_idx + 1,
                'machines': machines,
                'times': times
            })

    # Sort operations by shortest processing time and job id (due date proxy)
    operations.sort(key=lambda x: (min(x['times']), x['job_id']))

    # Schedule operations
    for operation in operations:
        job_id = operation['job_id']
        op_num = operation['operation_number']
        machines = operation['machines']
        times = operation['times']

        # Find the best machine and start time for the operation.
        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Update machine availability and job completion time.
        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job_id] = best_start_time + best_processing_time

        # Add operation to schedule.
        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

    return schedule
