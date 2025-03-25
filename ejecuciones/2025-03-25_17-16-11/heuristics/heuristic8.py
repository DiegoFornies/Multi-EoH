
def heuristic(input_data):
    """Heuristic for FJSSP: SPT with machine availability & job precedence."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    
    # Create a list of operations with their earliest start times and jobs
    operations = []
    for job, op_list in jobs.items():
        for op_idx, op in enumerate(op_list):
            operations.append({
                'job': job,
                'op_idx': op_idx,
                'machines': op[0],
                'times': op[1]
            })
    
    # Sort the operations based on the shortest processing time (SPT)
    operations.sort(key=lambda op: min(op['times']))  # sort by min processing time
    
    for op_data in operations:
        job = op_data['job']
        op_idx = op_data['op_idx']
        machines = op_data['machines']
        times = op_data['times']
        
        # Find the best machine based on earliest available time + processing time
        best_machine = None
        min_end_time = float('inf')
        
        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + times[m_idx]
            
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_time = times[m_idx]

        # Assign the operation to the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + best_time
        
        if job not in schedule:
            schedule[job] = []
            
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })
        
        # Update machine availability and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        
    return schedule
