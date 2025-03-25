
def heuristic(input_data):
    """FJSSP heuristic: SPT & least loaded machine with job completion."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in jobs}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)}

    operations = []
    for job_id in jobs:
        for op_idx, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, op_data))

    scheduled_operations = set()

    while len(scheduled_operations) < sum(len(ops) for ops in jobs.values()):
        best_operation = None
        min_score = float('inf')

        for job_id, op_idx, op_data in operations:
            if (job_id, op_idx) in scheduled_operations:
                continue

            preceding_operations_scheduled = all(
                (job_id, prev_op_idx) in scheduled_operations for prev_op_idx in range(op_idx)
            )
            if not preceding_operations_scheduled:
                continue

            machines, times = op_data
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                score = processing_time + machine_load[machine] * 0.1 + start_time * 0.05
                if score < min_score:
                    min_score = score
                    best_operation = (job_id, op_idx, machine, start_time, processing_time)

        if best_operation:
            job_id, op_idx, machine, start_time, processing_time = best_operation
            end_time = start_time + processing_time
            operation_number = op_idx + 1

            schedule[job_id].append({
                'Operation': operation_number,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = end_time
            job_completion_time[job_id] = end_time
            machine_load[machine] += processing_time
            scheduled_operations.add((job_id, op_idx))

        else:
            break

    return schedule
