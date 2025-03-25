
def heuristic(input_data):
    """Combines SPT, least utilized machine, and job completion time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    scheduled_operations = set()
    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, op_data))

    while len(scheduled_operations) < sum(len(ops) for ops in jobs.values()):
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
            if (job_id, op_idx) in scheduled_operations:
                continue
            
            preceding_operations_scheduled = True
            if op_idx > 0:
                if (job_id, op_idx - 1) not in scheduled_operations:
                    preceding_operations_scheduled = False

            if preceding_operations_scheduled:
                eligible_operations.append((job_id, op_idx, op_data))

        if not eligible_operations:
            break

        best_operation = None
        best_machine = None
        min_end_time = float('inf')
        best_start_time = None
        best_processing_time = None

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time
                #primary score
                load_factor = 0.1 * machine_load[machine]
                #secondary score
                score = end_time + load_factor

                if score < min_end_time:
                    min_end_time = score
                    best_machine = machine
                    best_operation = (job_id, op_idx, op_data)
                    best_start_time = start_time
                    best_processing_time = processing_time

        if best_operation:
            job_id, op_idx, op_data = best_operation
            end_time = best_start_time + best_processing_time
            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            scheduled_operations.add((job_id, op_idx))
            machine_load[best_machine] += best_processing_time

    return schedule
