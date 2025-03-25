
def heuristic(input_data):
    """A scheduling heuristic that minimizes makespan."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations by shortest processing time first (SPT)
    operations.sort(key=lambda x: min(x[3]))

    for job, op_num, machines, times in operations:
        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job])
            
            if start_time < best_start_time:
                best_machine, best_start_time, best_processing_time = machine, start_time, processing_time

        end_time = best_start_time + best_processing_time
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
