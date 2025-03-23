
def heuristic(input_data):
    """Combines SPT, load balancing, earliest finish for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job': job_id,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times
            })

    while operations:
        best_operation = None
        best_machine = None
        min_completion_time = float('inf')

        for operation in operations:
            job_id = operation['job']
            op_num = operation['operation']
            machines = operation['machines']
            times = operation['times']

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time
                load_penalty = machine_load[machine] * 0.001  # Scale down load penalty
                weighted_completion = 0.7 * end_time + 0.3 * load_penalty

                if weighted_completion < min_completion_time:
                    min_completion_time = weighted_completion
                    best_operation = operation
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

        job_id = best_operation['job']
        op_num = best_operation['operation']

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = best_start_time + best_processing_time
        machine_load[best_machine] += best_processing_time
        job_completion_time[job_id] = best_start_time + best_processing_time
        operations.remove(best_operation)

    return schedule
