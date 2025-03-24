
def heuristic(input_data):
    """Combines earliest completion time and operation priority."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}

    operations = []
    for job_id, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append((job_id, op_idx, machines, times))

    next_operation = {job_id: 0 for job_id in jobs_data}
    scheduled_operations = set()

    while len(scheduled_operations) < sum(len(ops) for ops in jobs_data.values()):
        best_op = None
        best_machine = None
        earliest_start = float('inf')

        for job_id in jobs_data:
            op_idx = next_operation[job_id]
            if op_idx >= len(jobs_data[job_id]):
                continue

            machines, times = jobs_data[job_id][op_idx]

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_op = (job_id, op_idx, machines, times)
                    best_machine = machine
                    processing_time = times[m_idx]

        if best_op is None:
            break

        job_id, op_idx, machines, times = best_op
        op_num = op_idx + 1

        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        scheduled_operations.add((job_id, op_idx))
        next_operation[job_id] += 1

    return schedule
