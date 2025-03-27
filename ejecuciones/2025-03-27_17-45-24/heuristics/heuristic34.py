
def heuristic(input_data):
    """Schedules FJSSP using a global optimization approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []

    # Create a list of all operations
    operations = []
    for job in range(1, n_jobs + 1):
        for op_idx in range(len(jobs_data[job])):
            operations.append((job, op_idx))

    # Schedule operations based on global makespan minimization
    for job, op_idx in operations:
        machines, times = jobs_data[job][op_idx]
        
        # Find machine and start time that minimizes global makespan
        best_machine = None
        min_end_time = float('inf')
        processing_time = 0
        start_time_chosen = 0
        
        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]
            start_time = max(machine_availability[machine], job_completion_times[job])
            end_time = start_time + time
            
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = time
                start_time_chosen = start_time
            
        # Schedule the operation
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time_chosen,
            'End Time': start_time_chosen + processing_time,
            'Processing Time': processing_time
        })

        # Update machine availability and job completion time
        machine_availability[best_machine] = start_time_chosen + processing_time
        job_completion_times[job] = start_time_chosen + processing_time

    return schedule
