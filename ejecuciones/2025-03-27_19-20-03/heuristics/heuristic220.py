
def heuristic(input_data):
    """Schedules jobs minimizing makespan and balancing machine load using shortest processing time and considering job slack."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    job_ops = {job: 0 for job in jobs}
    priority_list = []

    for job in jobs:
        ops = jobs[job]
        machines, times = ops[0]
        min_machine = machines[0]
        min_time = times[0]
        for m, t in zip(machines, times):
            if t < min_time:
                min_time = t
                min_machine = m
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
        min_load = float('inf')
        best_time = 0

        for m, t in zip(machines, times):
            start_time = max(machine_time[m], job_completion_time[job])
            load = machine_load[m] #Consider machine load to distribute work, balancing machine load
            
            if start_time < min_start_time or (start_time == min_start_time and load < min_load):
                min_start_time = start_time
                best_machine = m
                min_load = load
                best_time = t

        if best_machine is None:
            raise ValueError("No machine can be scheduled at the current moment. Bug in the optimization!")

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
            next_machines, next_times = jobs[job][job_ops[job]]
            min_machine = next_machines[0]
            min_time = next_times[0]
            for m, t in zip(next_machines, next_times):
                if t < min_time:
                    min_time = t
                    min_machine = m
            priority = job_completion_time[job] + min_time
            priority_list.append((priority, job))
            priority_list.sort()

    return schedule
