
def heuristic(input_data):
    """A heuristic using shortest processing time and machine utilization."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    job_ops = {job: 0 for job in jobs}
    available_operations = []

    for job in jobs:
        available_operations.append((0, job))

    while available_operations:
        # Sort available operations based on shortest processing time
        available_operations.sort(key=lambda x: min(input_data['jobs'][x[1]][x[0]][1]))

        op_idx, job = available_operations.pop(0)

        if job not in schedule:
            schedule[job] = []

        machines, times = jobs[job][op_idx]

        # Choose the machine with the earliest available time and lowest load.
        best_machine = None
        min_start_time = float('inf')

        for m, t in zip(machines, times):
            start_time = max(machine_time[m], job_completion_time[job])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = m
                best_time = t

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
        machine_load[best_machine] += best_time
        job_completion_time[job] = end_time

        job_ops[job] += 1

        if job_ops[job] < len(jobs[job]):
            available_operations.append((job_ops[job], job))

    return schedule
