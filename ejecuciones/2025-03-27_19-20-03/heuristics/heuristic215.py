
def heuristic(input_data):
    """Combines SPT and machine load balance for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}
    priority_queue = []

    # Initial priority: SPT + machine load consideration
    for job in jobs:
        ops = jobs[job]
        machines, times = ops[0]
        min_time = min(times)
        priority = (min_time / len(machines)) + (job/n_jobs) #Prioritize fast operations
        priority_queue.append((priority, job))

    priority_queue.sort()

    while priority_queue:
        priority, job = priority_queue.pop(0)

        if job not in schedule:
            schedule[job] = []

        op_idx = job_ops[job]
        machines, times = jobs[job][op_idx]

        best_machine = None
        min_start_time = float('inf')
        best_time = None

        # Prioritize machines with lower loads
        for m_idx, m in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_time[m], job_completion_time[job])
            # Load balancing term
            load_penalty = machine_load[m] / sum(machine_load.values()) if sum(machine_load.values())>0 else 0
            adjusted_start_time = start_time + load_penalty

            if adjusted_start_time < min_start_time:
                min_start_time = adjusted_start_time
                best_machine = m
                best_time = processing_time

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
            priority = job_completion_time[job] + (min_time / len(next_machines)) + (job/n_jobs) # slack = Finish_time + remaining_operation_time
            priority_queue.append((priority, job))
            priority_queue.sort()

    return schedule
