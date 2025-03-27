
def heuristic(input_data):
    """Schedules jobs using a Least Work Remaining (LWR) approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    remaining_work = {}

    # Calculate initial remaining work for each job.
    for job in range(1, n_jobs + 1):
        remaining_work[job] = sum(min(times) for machines, times in jobs[job])

    job_ops = {job: 0 for job in jobs}
    priority_list = []

    # Initial priority: Remaining Work
    for job in jobs:
        priority_list.append((remaining_work[job], job))

    priority_list.sort()

    while priority_list:
        priority, job = priority_list.pop(0)

        if job not in schedule:
            schedule[job] = []

        op_idx = job_ops[job]
        machines, times = jobs[job][op_idx]

        best_machine = None
        min_end_time = float('inf')
        best_time = None

        # Choose machine that results in the earliest end time.
        for m, t in zip(machines, times):
            start_time = max(machine_time[m], job_completion_time[job])
            end_time = start_time + t
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = m
                best_time = t

        if best_machine is None:
            raise ValueError("No feasible machine found for operation.")

        start_time = max(machine_time[best_machine], job_completion_time[job])
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

        # Update remaining work
        remaining_work[job] -= best_time
        job_ops[job] += 1

        if job_ops[job] < len(jobs[job]):
            priority = remaining_work[job]
            priority_list.append((priority, job))
            priority_list.sort()

    return schedule
