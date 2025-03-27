
def heuristic(input_data):
    """A scheduling heuristic minimizing makespan and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)} # Track machine load
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)} # Tracks last completion time of a job

    # Initialize job operation order and a priority list
    job_ops = {job: 0 for job in jobs}  # Next operation index for each job
    priority_list = [] # Contains (priority, job_id) tuples sorted to prioritize jobs with smaller slack time
    
    # Initially calculate priority, slack is finish time minus processing time
    for job in jobs:
        ops = jobs[job]
        machines, times = ops[0] # get feasible machines and processing times for first operation
        min_machine = machines[0]
        min_time = times[0]
        for m, t in zip(machines, times):
            if t < min_time:
                min_time = t
                min_machine = m
        priority = min_time
        priority_list.append((priority, job))
    
    priority_list.sort() # sort jobs initially on processing time of first operation

    while priority_list: # While there are unscheduled jobs
        priority, job = priority_list.pop(0) # take the highest priority job based on current operation

        if job not in schedule:
            schedule[job] = []
        
        op_idx = job_ops[job]
        machines, times = jobs[job][op_idx]

        # Choose the machine with the earliest available time, considering machine load balance.
        best_machine = None
        min_start_time = float('inf')
        
        # Iterate over all possible machines in a job and choose the one with minimal start time
        for m, t in zip(machines, times):
            #Consider machine time and job completion time
            start_time = max(machine_time[m], job_completion_time[job])

            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = m
                best_time = t
        
        # If no possible machine found
        if best_machine is None:
            raise ValueError("No machine can be scheduled at the current moment. Bug in the optimization!")
        
        start_time = min_start_time
        end_time = start_time + best_time
        
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })
        
        # Update machine time and machine load
        machine_time[best_machine] = end_time
        machine_load[best_machine] += best_time
        job_completion_time[job] = end_time

        # Advance to the next operation
        job_ops[job] += 1
        
        # If the job has more operations to schedule, calculate its new priority
        if job_ops[job] < len(jobs[job]):
            next_machines, next_times = jobs[job][job_ops[job]]
            min_machine = next_machines[0]
            min_time = next_times[0]
            for m, t in zip(next_machines, next_times):
                if t < min_time:
                    min_time = t
                    min_machine = m
            priority = job_completion_time[job] + min_time # slack = Finish_time + remaining_operation_time
            priority_list.append((priority, job))
            priority_list.sort() # maintain ordering
    
    return schedule
