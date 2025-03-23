
def heuristic(input_data):
    """Combines SPT and min workload to schedule jobs."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job': job_id,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times
            })

    operations.sort(key=lambda op: min(op['times']))

    for operation in operations:
        job_id = operation['job']
        op_num = operation['operation']
        machines = operation['machines']
        times = operation['times']

        best_machine = None
        min_end_time = float('inf')
        processing_time = 0

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_last_end_time[job_id])
            end_time = start_time + times[i]
            workload = machine_load[machine]

            combined_score = end_time + workload
            if combined_score < min_end_time:
                min_end_time = combined_score
                best_machine = machine
                processing_time = times[i]

        start_time = max(machine_available_time[best_machine], job_last_end_time[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        machine_load[best_machine] += processing_time
        job_last_end_time[job_id] = end_time

    return schedule
