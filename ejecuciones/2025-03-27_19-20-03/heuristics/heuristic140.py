
def heuristic(input_data):
    """Schedules jobs to minimize makespan and balance machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}
    priority_list = []

    # Initial priority: (operation_duration, machine_load, job_id)
    for job in jobs:
        ops = jobs[job]
        machines, times = ops[0]
        min_time = min(times)  # Find min processing time for the first operation.
        min_machine_index = times.index(min_time)
        min_machine = machines[min_machine_index]
        priority = (min_time, 0, job)  # Use processing time and initial machine load.
        priority_list.append(priority)

    import heapq
    heapq.heapify(priority_list)

    while priority_list:
        priority, load, job = heapq.heappop(priority_list)

        if job not in schedule:
            schedule[job] = []

        op_idx = job_ops[job]
        machines, times = jobs[job][op_idx]

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
        job_completion_time[job] = end_time

        job_ops[job] += 1

        if job_ops[job] < len(jobs[job]):
            next_machines, next_times = jobs[job][job_ops[job]]
            min_time = min(next_times)
            min_machine_index = next_times.index(min_time)
            min_machine = next_machines[min_machine_index]
            # Dynamically update the priority using job completion time and estimated processing time
            priority = (min_time + job_completion_time[job], machine_time[min_machine], job) # considering dynamic completion and machine utilization in heuristic
            heapq.heappush(priority_list, priority)

    return schedule
