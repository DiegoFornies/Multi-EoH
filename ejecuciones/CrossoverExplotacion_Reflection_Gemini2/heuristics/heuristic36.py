
def heuristic(input_data):
    """
    Heuristic for FJSSP that prioritizes operations with fewer machine options and shorter processing times.
    Minimizes makespan and balances machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of operations with their details
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx,
                'machines': op_data[0],
                'times': op_data[1]
            })

    # Sort operations by number of available machines and shortest processing time
    operations.sort(key=lambda op: (len(op['machines']), min(op['times'])))

    for operation in operations:
        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        # Find the best machine based on earliest available time
        best_machine = None
        min_start_time = float('inf')
        processing_time = 0

        for m_idx, machine in enumerate(machines):
            available_time = machine_available_times[machine]
            start_time = max(available_time, job_completion_times[job_id])
            
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                processing_time = times[m_idx]
        
        start_time = min_start_time
        end_time = start_time + processing_time

        # Update schedule, machine available time, and job completion time
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        
    return schedule
