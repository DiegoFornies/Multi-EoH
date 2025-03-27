
def heuristic(input_data):
    """Schedules jobs using priority and SPT for machine assignment."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}
    priority_list = []

    # Initial priority: (processing time / number of machines)
    for job in jobs:
        ops = jobs[job]
        machines, times = ops[0]
        min_time = min(times)
        priority = (min_time / len(machines))
        priority_list.append((priority, job))

    priority_list.sort()

    while priority_list:
        priority, job = priority_list.pop(0)

        if job not in schedule:
            schedule[job] = []

        op_idx = job_ops[job]
        machines, times = jobs[job][op_idx]

        # SPT selection for machine assignment
        best_machine = None
        min_end_time = float('inf')
        processing_time = None

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_time[machine], job_completion_time[job])
            end_time = start_time + times[m_idx]
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = times[m_idx]

        start_time = max(machine_time[best_machine], job_completion_time[job])
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_time[best_machine] = end_time
        job_completion_time[job] = end_time

        job_ops[job] += 1

        if job_ops[job] < len(jobs[job]):
            next_machines, next_times = jobs[job][job_ops[job]]
            min_time = min(next_times)
            priority = (min_time / len(next_machines)) + (job_completion_time[job]/1000)
            priority_list.append((priority, job))
            priority_list.sort()

    return schedule
