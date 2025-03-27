
def heuristic(input_data):
    """Schedules jobs minimizing makespan using a shortest processing time (SPT) rule."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of all operations with their properties
    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs[job_id]):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx,
                'machines': operation[0],
                'times': operation[1]
            })

    # Sort operations by shortest processing time
    operations.sort(key=lambda op: min(op['times']))

    # Schedule each operation
    for operation in operations:
        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        best_machine = None
        min_start_time = float('inf')
        best_time = None

        for m_idx, machine_id in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_time[machine_id], job_completion_time[job_id])

            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine_id
                best_time = processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        start_time = min_start_time
        end_time = start_time + best_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
