
def heuristic(input_data):
    """
    A heuristic for FJSSP that minimizes makespan by prioritizing operations
    with shorter processing times on less loaded machines.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of operations with job and operation indices
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, op_data))

    # Sort operations by shortest processing time first
    operations.sort(key=lambda x: min(x[2][1]))

    # Schedule operations
    for job_id, op_num, op_data in operations:
        machines, times = op_data

        # Find the machine with the earliest available time
        best_machine = None
        min_end_time = float('inf')
        best_time = None

        for i, m in enumerate(machines):
            start_time = max(machine_load[m], job_completion_times[job_id])
            end_time = start_time + times[i]
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = m
                best_time = times[i]
        
        start_time = max(machine_load[best_machine], job_completion_times[job_id])
        end_time = start_time + best_time
        
        # Update schedule
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine load and job completion time
        machine_load[best_machine] = end_time
        job_completion_times[job_id] = end_time
    return schedule
