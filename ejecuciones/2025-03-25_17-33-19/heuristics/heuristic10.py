
def heuristic(input_data):
    """
    A heuristic that prioritizes operations with fewer machine options
    and shorter processing times to balance machine load and reduce makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    
    # Create a list of operations with job and operation indices
    operations = []
    for job in jobs_data:
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            operations.append((job, op_idx, machines, times))

    # Sort operations based on the number of available machines (ascending)
    # and shortest processing time (ascending)
    operations.sort(key=lambda x: (len(x[2]), min(x[3])))

    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1
        best_machine, best_time, start_time = None, float('inf'), 0

        # Find the machine that minimizes the completion time of the operation
        for i, machine in enumerate(machines):
            available_time = machine_available_time[machine]
            start = max(available_time, job_completion_time[job])
            end = start + times[i]
            if end < best_time:
                best_machine, best_time, start_time = machine, end, start

        # Schedule the operation on the chosen machine
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': best_time,
            'Processing Time': times[machines.index(best_machine)]
        })

        # Update machine available time and job completion time
        machine_available_time[best_machine] = best_time
        job_completion_time[job] = best_time

    return schedule
