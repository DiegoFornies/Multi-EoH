
def heuristic(input_data):
    """Schedules jobs by earliest due date, minimizing makespan."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}

    job_due_dates = {}
    for job in range(1, n_jobs + 1):
        job_due_dates[job] = sum(min(times) for machines, times in jobs_data[job])

    job_queue = sorted(job_due_dates.keys(), key=job_due_dates.get)

    remaining_operations = {job: 1 for job in range(1, n_jobs + 1)}

    while job_queue:
        job = job_queue.pop(0)
        op_num = remaining_operations[job]

        if op_num > len(jobs_data[job]):
            continue
        machines, times = jobs_data[job][op_num - 1]

        best_machine = None
        min_end_time = float('inf')
        best_time = None

        for m_idx, m in enumerate(machines):
            start_time = max(machine_available_times[m], job_completion_times[job])
            end_time = start_time + times[m_idx]
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = m
                best_time = times[m_idx]

        start_time = max(machine_available_times[best_machine], job_completion_times[job])
        end_time = start_time + best_time

        scheduled_operations[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time
        remaining_operations[job] += 1

    return scheduled_operations
