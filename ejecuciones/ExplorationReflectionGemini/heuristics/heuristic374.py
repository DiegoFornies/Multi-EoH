
def heuristic(input_data):
    """Operation-centric scheduling using earliest start time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    operations = []
    for job_id, job_data in jobs.items():
        for op_num, (machines, times) in enumerate(job_data):
            operations.append({
                'job_id': job_id,
                'op_num': op_num + 1,
                'machines': machines,
                'times': times
            })

    while operations:
        best_op = None
        best_machine = None
        min_start_time = float('inf')

        for op in operations:
            job_id = op['job_id']
            machines = op['machines']
            times = op['times']
            
            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_times[job_id])
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_op = op
                    best_machine = machine
                    processing_time = times[i]

        if best_op:
            job_id = best_op['job_id']
            op_num = best_op['op_num']

            start_time = max(machine_available_time[best_machine], job_completion_times[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_times[job_id] = end_time
            operations.remove(best_op)

    return schedule
