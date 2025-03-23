
def heuristic(input_data):
    """
    Combines earliest finish time and shortest processing time for FJSSP.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    operations = []
    for job_id, job_ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job': job_id,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times
            })

    operations.sort(key=lambda op: min(op['times'])) #sort by shortest processing time

    for operation in operations:
        job_id = operation['job']
        op_num = operation['operation']
        machines = operation['machines']
        times = operation['times']

        best_machine = None
        min_end_time = float('inf')
        best_processing_time = None
        best_start_time = None

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time
                best_start_time = start_time

        if job_id not in schedule:
            schedule[job_id] = []

        machine_available_time[best_machine] = min_end_time
        job_completion_time[job_id] = min_end_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': min_end_time,
            'Processing Time': best_processing_time
        })

    return schedule
