
def heuristic(input_data):
    """Schedules jobs using a hybrid priority rule (LWKR+FIFO)."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}
    priority_queue = []

    # Initial priority: LWKR (Least Work Remaining) + FIFO
    for job in jobs:
        ops = jobs[job]
        remaining_work = sum(min(times) for machines, times in ops)
        priority = -remaining_work + (job/n_jobs)  # Negative since we want to schedule least work first
        priority_queue.append((priority, job))

    priority_queue.sort()

    while priority_queue:
        priority, job = priority_queue.pop(0)

        if job not in schedule:
            schedule[job] = []

        op_idx = job_ops[job]
        machines, times = jobs[job][op_idx]

        best_machine = None
        min_end_time = float('inf') #minimize end time

        for m_idx, m in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_time[m], job_completion_time[job])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = m
                best_time = processing_time
                best_start_time = start_time

        start_time = best_start_time
        end_time = best_start_time + best_time

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
            remaining_work = sum(min(times) for i, (machines, times) in enumerate(jobs[job]) if i >= job_ops[job] )
            priority = -remaining_work + (job/n_jobs) #LWKR
            priority_queue.append((priority, job))
            priority_queue.sort()

    return schedule
