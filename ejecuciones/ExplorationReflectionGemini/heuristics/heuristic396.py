
def heuristic(input_data):
    """Operation-centric scheduling with earliest start time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append({
                'job': job_id,
                'op_idx': op_idx,
                'machines': op_data[0],
                'times': op_data[1]
            })

    while operations:
        best_op = None
        best_machine = None
        earliest_start_time = float('inf')
        processing_time = None

        for op in operations:
            job_id = op['job']
            op_idx = op['op_idx']
            machines = op['machines']
            times = op['times']

            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_op = op
                    best_machine = machine
                    processing_time = times[i]

        if best_op is not None:
            job_id = best_op['job']
            op_idx = best_op['op_idx']
            op_num = op_idx + 1
            start_time = max(machine_available_time[best_machine], job_last_end_time[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            job_last_end_time[job_id] = end_time
            operations.remove(best_op)

    return schedule
