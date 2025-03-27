
def heuristic(input_data):
    """Schedules operations using a priority rule based on operation slack."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_remaining_time = {} #remaining time for each job.
    
    #initialize remaining time for each job.
    for job in jobs:
        total_time = 0
        for op_idx, op in enumerate(jobs[job]):
            total_time += min(op[1]) # use min time, since we want to have more conservative remaining time
        job_remaining_time[job] = total_time
    
    remaining_operations = {job: [i for i in range(len(ops))] for job, ops in jobs.items()}
    available_operations = []
    for job in jobs:
        if remaining_operations[job]:
            available_operations.append((job, remaining_operations[job][0]))
    
    while available_operations:
        # Select operation with smallest slack.
        best_op = None
        min_slack = float('inf')

        for job, op_idx in available_operations:
            machines, times = jobs[job][op_idx]
            
            #find the machine that provides the earliest possible start time for this operation
            best_machine = None
            min_start_time = float('inf')

            for m_idx, m in enumerate(machines):
                start_time = max(machine_time[m], job_completion_time[job])
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = m
                    best_time = times[m_idx]
            
            slack = min_start_time + best_time + job_remaining_time[job] - max(machine_time.values()) #min_start_time + best_time is the earliest the operation can finish.

            if slack < min_slack:
                min_slack = slack
                best_op = (job, op_idx, best_machine, best_time, min_start_time)

        job, op_idx, assigned_machine, processing_time, start_time = best_op
        end_time = start_time + processing_time

        if job not in schedule:
            schedule[job] = []
        
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        remaining_operations[job].pop(0)
        
        machine_time[assigned_machine] = end_time
        job_completion_time[job] = end_time
        job_remaining_time[job] -= processing_time

        if remaining_operations[job]:
            available_operations.append((job, remaining_operations[job][0]))

        available_operations.remove((job, op_idx))

    return schedule
