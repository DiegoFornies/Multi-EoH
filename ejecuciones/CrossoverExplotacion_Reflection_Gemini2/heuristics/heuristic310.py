
def heuristic(input_data):
    """Combines earliest finish time, machine load, and SPT."""
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
        # Select the operation with the shortest processing time from the available operations
        shortest_operation = min(operations, key=lambda op: min(op['times']))
        job_id = shortest_operation['job']
        op_num = shortest_operation['operation']
        machines = shortest_operation['machines']
        times = shortest_operation['times']

        best_machine = None
        min_end_time = float('inf')
        processing_time = 0

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + times[i]
            workload = machine_load[machine]
            weighted_end = 0.7 * end_time + 0.3 * workload #Weighting finish time and load
            if weighted_end < min_end_time:
                min_end_time = weighted_end
                best_machine = machine
                processing_time = times[i]

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        machine_load[best_machine] += processing_time
        job_completion_time[job_id] = end_time
        operations.remove(shortest_operation)

    return schedule
