
def heuristic(input_data):
    """Hybrid heuristic: SPT job order, earliest machine, and slack priority."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}

    job_remaining_times = {}
    for job, operations in jobs.items():
        total_time = sum(min(times) for machines, times in operations)
        job_remaining_times[job] = total_time

    job_order = sorted(job_remaining_times.keys(), key=job_remaining_times.get)

    priority_list = [(job_remaining_times[job], job) for job in job_order]

    while priority_list:
        priority, job = priority_list.pop(0)

        if job not in schedule:
            schedule[job] = []

        op_idx = job_ops[job]
        machines, times = jobs[job][op_idx]

        best_machine = None
        min_start_time = float('inf')
        best_time = None

        for m_idx, m in enumerate(machines):
            start_time = max(machine_time[m], job_completion_time[job])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = m
                best_time = times[m_idx]

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
        job_completion_time[job] = end_time
        job_ops[job] += 1

        if job_ops[job] < len(jobs[job]):
            next_machines, next_times = jobs[job][job_ops[job]]
            min_next_time = min(next_times)
            next_priority = job_completion_time[job] + min_next_time
            
            # Rebuild the list to avoid ordering complexities of re-inserting in the middle
            priority_list = []
            for j in job_order:
              if job_ops[j] < len(jobs[j]):
                next_machines_temp, next_times_temp = jobs[j][job_ops[j]]
                min_next_time_temp = min(next_times_temp)
                next_priority_temp = job_completion_time[j] + min_next_time_temp
                priority_list.append((next_priority_temp, j))

            priority_list.sort()
            
    return schedule
