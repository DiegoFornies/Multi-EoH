
def heuristic(input_data):
    """Combines earliest finish time and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}

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
        min_end_time = float('inf')

        for operation in operations:
            job_id = operation['job']
            op_num = operation['operation']
            machines = operation['machines']
            times = operation['times']

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available[machine], job_completion[job_id])
                end_time = start_time + processing_time
                workload = machine_load[machine]

                # Prioritize earliest finish time, break ties with lower machine load.
                if end_time + 0.0001 * workload < min_end_time:
                    min_end_time = end_time + 0.0001 * workload
                    best_operation = operation
                    best_machine = machine
                    best_processing_time = processing_time

        job_id = best_operation['job']
        op_num = best_operation['operation']

        start_time = max(machine_available[best_machine], job_completion[job_id])
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available[best_machine] = end_time
        machine_load[best_machine] += best_processing_time
        job_completion[job_id] = end_time
        operations.remove(best_operation)

    return schedule
