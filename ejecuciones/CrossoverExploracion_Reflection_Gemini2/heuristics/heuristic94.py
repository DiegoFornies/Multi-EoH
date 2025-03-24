
def heuristic(input_data):
    """FJSSP heuristic: Prioritize by processing time, break ties with earliest start."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of all operations with job and operation IDs
    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs_data[job_id]):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx + 1,
                'machines': operation[0],
                'times': operation[1]
            })

    # Schedule operations until all are scheduled
    while operations:
        best_op = None
        best_machine = None
        min_end_time = float('inf')

        # Find the best operation to schedule based on earliest possible end time
        for op in operations:
            job_id = op['job_id']
            op_idx = op['op_idx']
            machines = op['machines']
            times = op['times']

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_op = op
                    best_machine = machine
                    best_start_time = start_time
                    best_time = time

        # Schedule the best operation
        job_id = best_op['job_id']
        op_idx = best_op['op_idx']

        schedule[job_id].append({
            'Operation': op_idx,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': min_end_time,
            'Processing Time': best_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = min_end_time
        job_completion_time[job_id] = min_end_time

        # Remove the scheduled operation from the list of operations
        operations.remove(best_op)

    return schedule
