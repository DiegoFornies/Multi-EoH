
def heuristic(input_data):
    """Combines earliest finish time, SPT, and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    load_balancing_factor = 0.1

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job': job_id,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times,
                'processing_time': min(times)
            })

    operations.sort(key=lambda x: x['processing_time'])

    for operation in operations:
        job_id = operation['job']
        op_num = operation['operation']
        machines = operation['machines']
        times = operation['times']

        best_machine = None
        min_weighted_finish = float('inf')
        best_time = 0

        for i, machine in enumerate(machines):
            time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            finish_time = start_time + time
            weighted_finish = 0.7 * finish_time + 0.3 * machine_load[machine] * load_balancing_factor

            if weighted_finish < min_weighted_finish:
                min_weighted_finish = weighted_finish
                best_machine = machine
                best_time = time
                best_start = start_time

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        machine_load[best_machine] += best_time

    return schedule
