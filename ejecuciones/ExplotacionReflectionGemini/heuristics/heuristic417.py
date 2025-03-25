
def heuristic(input_data):
    """FJSSP heuristic: SPT, machine load, job completion."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    operations = []
    for job_id in jobs:
        for op_idx, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, op_data))

    scheduled_operations = set()

    while len(scheduled_operations) < sum(len(ops) for ops in jobs.values()):
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
            if job_id not in jobs:
                continue

            if (job_id, op_idx) in scheduled_operations:
                continue

            is_next_operation = True
            if op_idx > 0:
                if (job_id, op_idx - 1) not in scheduled_operations:
                    is_next_operation = False

            if is_next_operation:
                eligible_operations.append((job_id, op_idx, op_data))

        if not eligible_operations:
            break

        best_operation = None
        min_score = float('inf')
        best_machine = None
        best_start_time = None
        best_processing_time = None

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + time
                machine_load_factor = machine_load[machine]

                score = start_time + time + machine_load_factor # SPT, machine load, start

                if score < min_score:
                    min_score = score
                    best_operation = (job_id, op_idx, op_data)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = time

        if best_operation:
            job_id, op_idx, op_data = best_operation
            operation_number = op_idx + 1
            end_time = best_start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            machine_load[best_machine] += best_processing_time
            scheduled_operations.add((job_id, op_idx))
        else:
            break

    return schedule
