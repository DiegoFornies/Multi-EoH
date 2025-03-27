
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes jobs with fewer remaining operations."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs_data}
    remaining_ops = {job: len(ops) for job, ops in jobs_data.items()}  # Number of remaining operations for each job.
    scheduled_operations = {} # Save start and end operation's time for constraints
    
    completed_jobs = set()

    # Initialize schedule
    for job in jobs_data.keys():
        schedule[job] = []

    # Prioritize jobs with fewer remaining operations
    while len(completed_jobs) < n_jobs:
        eligible_jobs = [job for job in jobs_data if job not in completed_jobs]
        
        # Select the job with the fewest remaining operations
        job = min(eligible_jobs, key=lambda j: remaining_ops[j])
        
        # Get the index of the next operation for the selected job
        op_idx = len(schedule[job])
        
        # If the job is complete, skip it
        if op_idx >= len(jobs_data[job]):
            completed_jobs.add(job)
            continue
        
        # Get the next operation
        machines, times = jobs_data[job][op_idx]
        op_num = op_idx + 1

        # Find the machine with the earliest available time
        best_machine, best_start, best_time = None, float('inf'), None
        for m, t in zip(machines, times):
            start = max(machine_time[m], job_completion_times[job])
            if start < best_start:
                best_start, best_machine, best_time = start, m, t

        start = best_start
        end = start + best_time
        m = best_machine
        t = best_time
    
        # Add operation to the schedule
        schedule[job].append({'Operation': op_num, 'Assigned Machine': m, 'Start Time': start, 'End Time': end, 'Processing Time': t})
        
        # Update machine time and job completion time
        machine_time[m] = end
        job_completion_times[job] = end
        
        # Decrement the remaining operations count
        remaining_ops[job] -= 1
        
        # Check if the job is complete
        if remaining_ops[job] == 0:
            completed_jobs.add(job)
    
    return schedule
