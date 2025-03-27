
def heuristic(input_data):
    """Schedules jobs based on machine idleness."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}

    unassigned_jobs = list(range(1, n_jobs + 1))

    while unassigned_jobs:
        job = unassigned_jobs.pop(0)
        if job not in schedule:
            schedule[job] = []

        op_idx = job_ops[job]
        machines, times = jobs[job][op_idx]
        
        best_machine = None
        min_idle_time = float('inf')
        best_processing_time = None

        for m_idx, m in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_time[m], job_completion_time[job])
            idle_time = start_time - machine_time[m] if start_time > machine_time[m] else 0

            if idle_time < min_idle_time:
                min_idle_time = idle_time
                best_machine = m
                best_processing_time = processing_time

        start_time = max(machine_time[best_machine], job_completion_time[job])
        end_time = start_time + best_processing_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_time[best_machine] = end_time
        job_completion_time[job] = end_time
        job_ops[job] += 1

        if job_ops[job] < len(jobs[job]):
            unassigned_jobs.insert(0, job)
        
    return schedule
