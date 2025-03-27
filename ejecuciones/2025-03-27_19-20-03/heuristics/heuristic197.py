
def heuristic(input_data):
    """Combines EDD, SPT, and machine load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}

    job_priorities = {}
    for job in jobs:
        job_priorities[job] = 0
        for machines, times in jobs[job]:
            job_priorities[job] += min(times)  # EDD component
    job_queue = sorted(jobs.keys(), key=lambda job: job_priorities[job])

    while job_queue:
        job = job_queue.pop(0)
        if job not in schedule:
            schedule[job] = []

        op_idx = job_ops[job]
        machines, times = jobs[job][op_idx]
        best_machine = None
        min_end_time = float('inf')

        for m, t in zip(machines, times):
            start_time = max(machine_time[m], job_completion_time[job])
            end_time = start_time + t
            load_factor = machine_load[m] # SPT component

            # Consider machine load and earliest finish time
            if end_time + load_factor*0.001 < min_end_time: #added machine load influence factor.
                min_end_time = end_time
                best_machine = m
                best_time = t

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
        machine_load[best_machine] += best_time
        job_completion_time[job] = end_time
        job_ops[job] += 1
        if job_ops[job] < len(jobs[job]):
            job_queue.append(job)
            remaining_time = sum(min(times) for machines, times in jobs[job][job_ops[job]:])
            job_queue.sort(key=lambda job: job_completion_time[job] + remaining_time) #EDD

    return schedule
