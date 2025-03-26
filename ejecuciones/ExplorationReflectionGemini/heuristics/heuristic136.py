
def heuristic(input_data):
    """Prioritizes jobs based on remaining work and selects the fastest machine."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    remaining_work = {j: sum(min(times) for machines, times in jobs[j]) for j in jobs}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        # Select operation with max remaining work
        best_op = None
        max_remaining_work = float('-inf')

        for op_data in available_operations:
            job_id = op_data['job']
            if remaining_work[job_id] > max_remaining_work:
                max_remaining_work = remaining_work[job_id]
                best_op = op_data

        job_id = best_op['job']
        op_idx = best_op['op_idx']
        machines, times = jobs[job_id][op_idx]

        # Find the machine that allows for the earliest finish time
        best_machine = None
        min_end_time = float('inf')
        processing_time = None

        for machine_idx, (machine, time) in enumerate(zip(machines, times)):
            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            end_time = start_time + time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = time

        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + processing_time
        op_num = op_idx + 1

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        remaining_work[job_id] -= processing_time

        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
