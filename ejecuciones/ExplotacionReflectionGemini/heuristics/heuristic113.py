
def heuristic(input_data):
    """Combines SPT and machine load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    for job in jobs:
        schedule[job] = []

    scheduled_operations = set()
    operations = []
    for job_id in jobs:
        for op_idx, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, op_data))

    while len(scheduled_operations) < sum(len(ops) for ops in jobs.values()):
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
            if (job_id, op_idx) in scheduled_operations:
                continue
            preceding_operations_scheduled = all((job_id, prev_op_idx) in scheduled_operations for prev_op_idx in range(op_idx))
            if preceding_operations_scheduled:
                eligible_operations.append((job_id, op_idx, op_data))

        if not eligible_operations:
            break

        best_operation = None
        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        for job_id, op_idx, (machines, times) in eligible_operations:
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time + processing_time < best_start_time + (best_processing_time if best_processing_time else float('inf')):
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
                    best_operation = (job_id, op_idx, machines, times)

        if best_operation:
            job_id, op_idx, machines, times = best_operation
            machine = best_machine
            processing_time = best_processing_time
            start_time = best_start_time
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
            scheduled_operations.add((job_id, op_idx))

    return schedule
