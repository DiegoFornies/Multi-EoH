
def heuristic(input_data):
    """Operation-centric heuristic for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    operations = []
    for job, op_list in jobs.items():
        for i, op_data in enumerate(op_list):
            operations.append((job, i, op_data))

    operations.sort(key=lambda x: min(x[2][1]))

    for job, op_index, op_data in operations:
        machines, times = op_data
        op_num = op_index + 1

        best_machine, min_end_time, processing_time = None, float('inf'), None
        for i, m in enumerate(machines):
            start_time = max(job_completion_times[job], machine_available_times[m])
            end_time = start_time + times[i]

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = m
                processing_time = times[i]

        if best_machine is not None:
            start_time = max(job_completion_times[job], machine_available_times[best_machine])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_times[best_machine] = end_time
            job_completion_times[job] = end_time

    return schedule
