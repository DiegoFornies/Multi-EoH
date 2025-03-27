
def heuristic(input_data):
    """Schedules jobs minimizing makespan, considering machine load and job slack."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}
    priority_list = []

    # Initial priority: Earliest Finish Time (EFT)
    for job in jobs:
        ops = jobs[job]
        machines, times = ops[0]
        best_machine = None
        min_finish_time = float('inf')
        for m, t in zip(machines, times):
            finish_time = machine_time[m] + t # Considering machine availability
            if finish_time < min_finish_time:
                min_finish_time = finish_time
                best_machine = m
                best_time = t
        if best_machine is None:
          priority=0
        else:
          priority = min_finish_time
        priority_list.append((priority, job))

    priority_list.sort()

    while priority_list:
        priority, job = priority_list.pop(0)

        if job not in schedule:
            schedule[job] = []

        op_idx = job_ops[job]
        machines, times = jobs[job][op_idx]

        # Machine selection: Balance load and minimize start time
        best_machine = None
        min_start_time = float('inf')
        load_penalty = 0.001  # Small penalty to favor less loaded machines

        for m, t in zip(machines, times):
            start_time = max(machine_time[m], job_completion_time[job])
            # Prioritize machines with lower loads by adding a load-based penalty
            start_time += machine_load[m] * load_penalty

            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = m
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

        # Update priority: EFT for next operation
        if job_ops[job] < len(jobs[job]):
            next_machines, next_times = jobs[job][job_ops[job]]
            best_machine = None
            min_finish_time = float('inf')

            for m, t in zip(next_machines, next_times):
                finish_time = max(machine_time[m],job_completion_time[job]) + t #machine_time[m] + t
                if finish_time < min_finish_time:
                    min_finish_time = finish_time
                    best_machine = m
            if best_machine is None:
              priority=0
            else:
              priority = min_finish_time
            priority_list.append((priority, job))
            priority_list.sort()

    return schedule
