
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes shortest processing time and machine availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(1, n_machines + 1)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    operations = []
    for job, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations based on shortest processing time
    operations.sort(key=lambda x: min(x[3]))

    for job, op_num, machines, times in operations:
        best_machine, best_time, best_start_time = None, float('inf'), None
        
        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])

            if start_time + processing_time < best_time:
                best_machine, best_time, best_start_time = machine, start_time + processing_time, start_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_time,
            'Processing Time': best_time - best_start_time
        })
        machine_available_time[best_machine] = best_time
        job_completion_time[job] = best_time
    return schedule
