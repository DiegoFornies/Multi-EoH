
def heuristic(input_data):
    """Schedule using Shortest Processing Time and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {j: 0 for j in range(1, n_jobs + 1)}

    available_ops = []
    for job_id in jobs:
        available_ops.append((min(jobs[job_id][0][1]), job_id)) # (SPT, job_id)

    while available_ops:
        available_ops.sort()
        _, job_id = available_ops.pop(0)

        if job_id not in schedule:
            schedule[job_id] = []

        op_idx = job_ops[job_id]
        machines, times = jobs[job_id][op_idx]

        best_machine = None
        min_end_time = float('inf')

        for m, t in zip(machines, times):
            start_time = max(machine_time[m], job_completion[job_id])
            end_time = start_time + t
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = m
                best_time = t

        start_time = max(machine_time[best_machine], job_completion[job_id])
        end_time = start_time + best_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_time[best_machine] = end_time
        job_completion[job_id] = end_time
        job_ops[job_id] += 1

        if job_ops[job_id] < len(jobs[job_id]):
            available_ops.append((min(jobs[job_id][job_ops[job_id]][1]), job_id))

    return schedule
