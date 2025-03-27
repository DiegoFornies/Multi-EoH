
def heuristic(input_data):
    """Heuristic for FJSSP: Shortest Processing Time first on Least Loaded Machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Flatten operations into a list for sorting
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations by shortest processing time
    operations.sort(key=lambda x: min(x[3]))  # x[3] are times
    
    for job, op_idx, machines, times in operations:
        # Find the machine with the earliest available time for the operation
        best_machine = None
        min_start_time = float('inf')
        
        for m_idx, machine in enumerate(machines):
            machine_start_time = machine_load[machine]
            job_ready_time = job_completion_times[job]
            start_time = max(machine_start_time, job_ready_time)
            
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_time_index = m_idx
                

        processing_time = times[best_time_index]
        start_time = min_start_time
        end_time = start_time + processing_time

        # Update schedule
        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine load and job completion time
        machine_load[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
