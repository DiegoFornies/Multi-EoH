
def heuristic(input_data):
    """
    Heuristic to solve FJSSP by prioritizing operations with fewer machine choices and shortest processing time.
    Balances machine load by selecting the machine with the earliest available time for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    schedule = {}
    
    # Create a list of operations to schedule, including job and operation indices
    operations = []
    for job in jobs_data:
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            operations.append((job, op_idx, machines, times))
    
    # Sort operations by number of possible machines (ascending) and shortest processing time (ascending)
    operations.sort(key=lambda x: (len(x[2]), min(x[3])))
    
    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1
        
        # Find the machine with the earliest available time
        best_machine = None
        min_end_time = float('inf')
        
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + times[i]
            
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = times[i]
        
        # Schedule the operation on the selected machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + best_processing_time
        
        if job not in schedule:
            schedule[job] = []
        
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        
    return schedule
