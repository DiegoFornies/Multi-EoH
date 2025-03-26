
def heuristic(input_data):
    """Minimizes makespan by prioritizing shortest processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    operations = []
    for job in range(1, n_jobs + 1):
        for op_idx, (machines, times) in enumerate(jobs[job]):
            operations.append((job, op_idx, machines, times))

    # Sort operations by shortest processing time
    eligible_ops = []
    for job, op_idx, machines, times in operations:
        min_time = float('inf')
        for time in times:
            if time < min_time:
                min_time = time
        eligible_ops.append(((job, op_idx, machines, times),min_time))
        
    eligible_ops.sort(key = lambda x: x[1])

    for ((job, op_idx, machines, times), min_time) in eligible_ops:
        best_machine = None
        min_end_time = float('inf')

        for i, machine in enumerate(machines):
            start_time = max(machine_time[machine], job_completion_time[job])
            end_time = start_time + times[i]
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = times[i]

        machine_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job] = best_start_time + best_processing_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

    return schedule
