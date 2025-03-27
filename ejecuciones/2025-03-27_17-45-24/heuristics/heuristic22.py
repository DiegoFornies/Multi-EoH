
def heuristic(input_data):
    """
    A simple heuristic for the FJSSP that prioritizes machines
    with the earliest available time and jobs with the shortest
    remaining processing time to balance machine load and reduce makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize schedule and machine availability
    schedule = {}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    remaining_times = {}

    for job, ops in jobs_data.items():
        remaining_times[job] = sum(times[0] for _, times in ops)
    
    completed_operations = {job: 0 for job in range(1, n_jobs + 1)}
    
    # Schedule operations
    while any(completed_operations[job] < len(jobs_data[job]) for job in range(1, n_jobs+1)):
        eligible_operations = []
        for job in range(1, n_jobs + 1):
            if completed_operations[job] < len(jobs_data[job]):
                eligible_operations.append(job)
        
        # Prioritize jobs with the shortest remaining processing time
        job = min(eligible_operations, key=lambda j: remaining_times[j])

        op_idx = completed_operations[job]
        machines, times = jobs_data[job][op_idx]
        
        # Find the machine with the earliest available time among feasible ones
        best_machine = None
        min_start_time = float('inf')
        processing_time = float('inf')
        
        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]
            
            start_time = max(machine_availability[machine], job_completion_times[job])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                processing_time = time
                
            elif start_time == min_start_time and time < processing_time:
                best_machine = machine
                processing_time = time
        
        start_time = max(machine_availability[best_machine], job_completion_times[job])
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
        
        # Update machine availability and job completion time
        machine_availability[best_machine] = end_time
        job_completion_times[job] = end_time
        remaining_times[job] -= processing_time
        completed_operations[job] += 1
        
    return schedule
