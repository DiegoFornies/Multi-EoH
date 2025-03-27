
def heuristic(input_data):
    """Schedules jobs minimizing makespan using priority and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}
    priority_list = []

    for job in jobs:
        ops = jobs[job]
        machines, times = ops[0]
        min_time = min(times)
        priority = min_time
        priority_list.append((priority, job))

    priority_list.sort()

    while priority_list:
        priority, job = priority_list.pop(0)

        if job not in schedule:
            schedule[job] = []

        op_idx = job_ops[job]
        machines, times = jobs[job][op_idx]

        best_machine = None
        min_start_time = float('inf')

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_time[machine], job_completion_time[job])

            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_time = times[m_idx]

        if best_machine is None:
            raise ValueError("No machine can be scheduled at the current moment.")

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
            priority = job_completion_time[job] + min_time
            priority_list.append((priority, job))
            priority_list.sort()

    return schedule
