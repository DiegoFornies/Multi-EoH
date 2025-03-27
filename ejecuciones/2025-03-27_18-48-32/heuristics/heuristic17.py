
def heuristic(input_data):
    """A heuristic to solve the FJSSP by prioritizing operations with fewer machine options."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    
    # Create a list of operations with their job and operation number
    operations = []
    for job, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append((job, op_idx + 1, machines, times)) # job, op_num, machines, times
    
    # Sort operations based on the number of available machines (least first)
    operations.sort(key=lambda x: len(x[2]))
    
    for job, op_num, machines, times in operations:
        # Find the earliest available machine and time for this operation
        best_machine, start_time, processing_time = None, float('inf'), None
        
        for m_idx, machine in enumerate(machines):
            #Consider time between job completion time and machine availability. 
            start = max(machine_available_time[machine], job_completion_time[job]) 
            if start < start_time:
                start_time = start
                best_machine = machine
                processing_time = times[m_idx]
        
        # Schedule the operation on the best machine
        if job not in schedule:
            schedule[job] = []
        
        end_time = start_time + processing_time
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        
    return schedule
