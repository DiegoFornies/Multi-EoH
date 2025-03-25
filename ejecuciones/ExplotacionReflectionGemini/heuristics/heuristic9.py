
def heuristic(input_data):
    """A scheduling heuristic that prioritizes short operations and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    # Create a list of all operations with relevant information
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op in enumerate(job_ops):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx,
                'machines': op[0],
                'times': op[1]
            })

    # Sort operations by shortest processing time
    operations.sort(key=lambda op: min(op['times']))

    for operation in operations:
        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        best_machine = -1
        min_end_time = float('inf')
        best_processing_time = -1

        # Find the best machine to minimize completion time
        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_processing_time
        op_num = op_idx + 1

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
