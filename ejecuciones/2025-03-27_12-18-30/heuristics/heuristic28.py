
def heuristic(input_data):
    """
    Schedules jobs minimizing makespan using a greedy approach.
    It prioritizes operations with shorter processing times and
    assigns them to the earliest available machine to reduce idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}  # Stores the schedule for each job
    machine_available_times = {m: 0 for m in range(n_machines)} # Earliest available time for each machine
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)} # Completion time of each job so far
    
    # Create a list of operations to schedule, with information about the job, operation index, possible machines, and times
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job': job_id,
                'op_idx': op_idx,
                'machines': machines,
                'times': times
            })
            
    # Sort operations by shortest processing time first (SPT)
    operations.sort(key=lambda op: min(op['times']))

    for operation in operations:
        job_id = operation['job']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        # Find the best machine to minimize completion time
        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job_id])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Assign operation to the best machine
        start_time = best_start_time
        end_time = start_time + best_processing_time

        # Update machine and job completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

        # Add the operation to the schedule
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
    return schedule
