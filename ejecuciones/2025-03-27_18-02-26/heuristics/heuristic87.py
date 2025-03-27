
def heuristic(input_data):
    """A heuristic for FJSSP using Shortest Processing Time (SPT) rule."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, operation in enumerate(job_ops):
            machines, processing_times = operation
            min_time = float('inf')
            best_machine = None
            best_processing_time = None

            for machine, time in zip(machines, processing_times):
                if time < min_time:
                    min_time = time
                    best_machine = machine
                    best_processing_time = time

            operations.append({
                'job_id': job_id,
                'op_idx': op_idx,
                'machine': best_machine,
                'processing_time': best_processing_time
            })

    # Sort operations by processing time (SPT)
    operations.sort(key=lambda x: x['processing_time'])

    for operation in operations:
        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machine = operation['machine']
        processing_time = operation['processing_time']

        start_time = max(machine_time[machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_time[machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
