
def heuristic(input_data):
    """Minimize makespan using longest processing time first."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    op_idx = {job: 0 for job in jobs}
    queue = []

    for job in jobs:
        ops = jobs[job]
        machines, times = ops[0]
        max_time = 0
        for t in times:
            if t > max_time:
                max_time = t
        queue.append((-max_time, job)) # Longest processing time first
    queue.sort()

    while queue:
        _, job = queue.pop(0)
        if job not in schedule:
            schedule[job] = []

        curr_op = op_idx[job]
        machines, times = jobs[job][curr_op]

        best_machine = None
        min_start_time = float('inf')
        best_time = None

        for m, t in zip(machines, times):
            start_time = max(machine_time[m], job_completion[job])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = m
                best_time = t

        start_time = min_start_time
        end_time = start_time + best_time

        schedule[job].append({
            'Operation': curr_op + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_time[best_machine] = end_time
        job_completion[job] = end_time
        op_idx[job] += 1

        if op_idx[job] < len(jobs[job]):
            machines, times = jobs[job][op_idx[job]]
            max_time = 0
            for t in times:
                if t > max_time:
                    max_time = t
            queue.append((-max_time, job))
            queue.sort()
    return schedule
