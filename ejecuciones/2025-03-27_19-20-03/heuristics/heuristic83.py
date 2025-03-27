
def heuristic(input_data):
    """Schedules jobs minimizing makespan, balancing machine load using combined priority."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}
    priority_list = []

    # Combined priority: (processing time / # of machines) + job_id + completion time
    for job in jobs:
        ops = jobs[job]
        machines, times = ops[0]
        min_time = min(times)
        priority = (min_time / len(machines)) + (job / n_jobs)
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
        best_time = None

        # Prioritize machines with lower loads.
        for m, t in zip(machines, times):
            start_time = max(machine_time[m], job_completion_time[job])
            load_penalty = machine_load[m] / sum(machine_load.values()) if sum(machine_load.values()) > 0 else 0
            adjusted_start_time = start_time + load_penalty

            if adjusted_start_time < min_start_time:
                min_start_time = adjusted_start_time
                best_machine = m
                best_time = t

        if best_machine is None:
            raise ValueError("No machine can be scheduled!")

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
            next_machines, next_times = jobs[job][job_ops[job]]
            min_time = min(next_times)
            priority = job_completion_time[job] + (min_time / len(next_machines)) + (job / n_jobs)
            priority_list.append((priority, job))
            priority_list.sort()

    return schedule
