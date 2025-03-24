
def heuristic(input_data):
    """Prioritize jobs with fewer remaining operations and machines with earlier availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []

    runnable_operations = []
    for job in range(1, n_jobs + 1):
        runnable_operations.append((job, 0))

    while runnable_operations:
        best_op = None
        best_machine = None
        min_completion_time = float('inf')

        for job, op_idx in runnable_operations:
            machines, times = jobs_data[job][op_idx]
            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + times[i]
                remaining_ops = sum(1 for j, idx in runnable_operations if j == job)
                priority = end_time + remaining_ops * 10 #prioritize smaller end_time and small operations remaining
                if priority < min_completion_time:
                    min_completion_time = priority
                    best_op = (job, op_idx)
                    best_machine = machine
                    processing_time = times[i]
                    start_time_best = start_time

        job, op_idx = best_op
        op_num = op_idx + 1

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time_best,
            'End Time': start_time_best + processing_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = start_time_best + processing_time
        job_completion_time[job] = start_time_best + processing_time

        runnable_operations.remove((job, op_idx))

        if op_idx + 1 < len(jobs_data[job]):
            runnable_operations.append((job, op_idx + 1))

    return schedule
