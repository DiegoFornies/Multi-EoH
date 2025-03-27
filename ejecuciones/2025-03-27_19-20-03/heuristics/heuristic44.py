
def heuristic(input_data):
    """Schedule jobs using a shortest processing time and earliest start time rule."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}
    ready_operations = []

    # Initially, add first operation of each job to ready_operations
    for job in jobs:
        machines, times = jobs[job][0]
        min_time = min(times)
        ready_operations.append((min_time, job, 0))  # (processing_time, job_id, operation_index)
    ready_operations.sort()

    while ready_operations:
        processing_time, job, op_idx = ready_operations.pop(0)

        if job not in schedule:
            schedule[job] = []

        machines, times = jobs[job][op_idx]

        best_machine = None
        min_start_time = float('inf')

        for m_idx, m in enumerate(machines):
            current_processing_time = times[m_idx]
            start_time = max(machine_time[m], job_completion_time[job])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = m
                best_time = current_processing_time

        start_time = min_start_time
        end_time = start_time + best_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_time[best_machine] = end_time
        job_completion_time[job] = end_time
        job_ops[job] += 1

        if job_ops[job] < len(jobs[job]):
            next_machines, next_times = jobs[job][job_ops[job]]
            min_time = min(next_times)
            ready_operations.append((min_time, job, job_ops[job]))
            ready_operations.sort()

    return schedule
