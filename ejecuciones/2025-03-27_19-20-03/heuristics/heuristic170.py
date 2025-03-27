
def heuristic(input_data):
    """Schedules jobs considering machine load and job dependencies,
    prioritizing shortest processing time and earliest start time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}
    
    # Use a list of tuples (priority, job) for active jobs
    active_jobs = []
    for job in jobs:
        active_jobs.append((0,job)) # initial priority does not matter since sorting happens in the loop.
        

    while active_jobs:
        # Choose job based on priority, shortest processing time and earliest available machine
        best_job = None
        min_priority = float('inf')
        
        for priority, job in active_jobs:
            op_idx = job_ops[job]
            machines, times = jobs[job][op_idx]
            
            # Find the best machine for the current job
            best_machine_job = None
            min_start_time_job = float('inf')
            
            for m, t in zip(machines, times):
                start_time = max(machine_time[m], job_completion_time[job])
                if start_time < min_start_time_job:
                    min_start_time_job = start_time
                    best_machine_job = m
                    best_time_job = t
            
            if best_machine_job is not None:
                # Calculate a new priority based on start time and process time
                current_priority = min_start_time_job + best_time_job
                if current_priority < min_priority:
                    min_priority = current_priority
                    best_job = job
        
        # If no job can be scheduled at the current moment
        if best_job is None:
            raise ValueError("No job can be scheduled at the current moment. Check code.")
        
        # Remove best job from the active jobs and add it back later (if it still has operations)
        priority_remove_idx = None
        for idx, item in enumerate(active_jobs):
            if item[1] == best_job:
                priority_remove_idx = idx
                break
        if priority_remove_idx is not None:
            del active_jobs[priority_remove_idx]

        # Get the best machine for the best job
        op_idx = job_ops[best_job]
        machines, times = jobs[best_job][op_idx]
        
        best_machine = None
        min_start_time = float('inf')
        for m, t in zip(machines, times):
            start_time = max(machine_time[m], job_completion_time[best_job])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = m
                best_time = t
        
        start_time = min_start_time
        end_time = start_time + best_time
        
        if best_job not in schedule:
            schedule[best_job] = []
            
        schedule[best_job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })
        
        machine_time[best_machine] = end_time
        job_completion_time[best_job] = end_time
        job_ops[best_job] += 1
        
        # Re-add job if there are remaining operations
        if job_ops[best_job] < len(jobs[best_job]):
            active_jobs.append((0, best_job))

    return schedule
