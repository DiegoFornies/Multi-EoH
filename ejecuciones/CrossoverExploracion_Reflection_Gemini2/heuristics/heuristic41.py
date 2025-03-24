
def heuristic(input_data):
    """Combines SPT and earliest start, prioritizing fewer machine options."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    remaining_operations = []
    for job_id, operations in jobs_data.items():
        for op_idx, operation in enumerate(operations):
            remaining_operations.append((job_id, op_idx))

    while remaining_operations:
        best_op = None
        best_machine = None
        min_end_time = float('inf')
        fewest_machines = float('inf')

        for job_id, op_idx in remaining_operations:
            machines, times = jobs_data[job_id][op_idx]

            if len(machines) < fewest_machines:
                fewest_machines = len(machines)

        candidates = []
        for job_id, op_idx in remaining_operations:
            machines, times = jobs_data[job_id][op_idx]
            if len(machines) == fewest_machines:
                candidates.append((job_id, op_idx))

        for job_id, op_idx in candidates:
            machines, times = jobs_data[job_id][op_idx]
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_op = (job_id, op_idx)
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

        if best_op is None:
            break

        job_id, op_idx = best_op
        op_num = op_idx + 1

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': min_end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = min_end_time
        job_completion_time[job_id] = min_end_time
        remaining_operations.remove((job_id, op_idx))

    return schedule
