
def heuristic(input_data):
    """
    A heuristic for FJSSP scheduling that prioritizes shorter operations
    and balances machine workload.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Flatten operations and sort by processing time
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx + 1,
                'machines': machines,
                'times': times
            })

    operations.sort(key=lambda op: min(op['times']))

    for operation in operations:
        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        best_machine = None
        min_end_time = float('inf')

        # Find the machine that results in the earliest completion time
        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        # Schedule the operation on the selected machine
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': min_end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = min_end_time
        job_completion_time[job_id] = min_end_time

    return schedule
