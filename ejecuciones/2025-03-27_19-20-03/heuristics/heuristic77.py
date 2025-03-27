
def heuristic(input_data):
    """Schedules jobs using a shortest remaining processing time (SRPT) rule."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    remaining_times = {}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        remaining_times[job] = sum(min(times) for machines, times in jobs_data[job])

    eligible_operations = []
    for job in range(1, n_jobs + 1):
        eligible_operations.append((remaining_times[job], job, 0))

    eligible_operations.sort()

    scheduled_ops = {job: 0 for job in range(1, n_jobs + 1)}

    while eligible_operations:
        _, job, op_idx = eligible_operations.pop(0)

        machines, times = jobs_data[job][op_idx]
        best_machine, best_time, best_processing_time = None, float('inf'), None

        for m_idx, machine in enumerate(machines):
            available_time = max(machine_available_time[machine], job_completion_time[job])
            if available_time < best_time:
                best_machine = machine
                best_time = available_time
                best_processing_time = times[m_idx]

        start_time = best_time
        processing_time = best_processing_time
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        scheduled_ops[job] += 1

        if scheduled_ops[job] < len(jobs_data[job]):
            next_op_idx = scheduled_ops[job]
            remaining_times[job] -= min(times for machines, times in [jobs_data[job][op_idx]])
            remaining_times[job] += min(times for machines, times in [jobs_data[job][next_op_idx]])
            eligible_operations.append((remaining_times[job], job, next_op_idx))
            eligible_operations.sort()

    return schedule
