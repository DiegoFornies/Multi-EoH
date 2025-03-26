
def heuristic(input_data):
    """Hybrid heuristic: SPT+least loaded machine, prioritizing critical ops."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs_data}

    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append({
                'job': job,
                'op_idx': op_idx,
                'machines': machines,
                'times': times,
                'priority': len(machines),
            })

    operations.sort(key=lambda x: (x['job'], x['op_idx'], x['priority']))

    schedule = {job: [] for job in jobs_data}

    for op in operations:
        job = op['job']
        op_idx = op['op_idx']
        machines = op['machines']
        times = op['times']

        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None
        min_load = float('inf')

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_availability[machine], job_completion_times[job])
            load = machine_availability[machine]

            if load < min_load:
                min_load = load
                if start_time < best_start_time:
                  best_start_time = start_time
                  best_machine = machine
                  best_processing_time = processing_time

        end_time = best_start_time + best_processing_time
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_availability[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
