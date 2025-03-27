
def heuristic(input_data):
    """
    Heuristic for FJSSP minimizing makespan, idle time, and balancing machine load.
    Prioritizes operations with fewer machine options and shorter processing times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Create a list of operations with job and operation indices
    operations = []
    for job_id, operations_list in jobs_data.items():
        for op_idx, op_data in enumerate(operations_list):
            operations.append((job_id, op_idx + 1, op_data))
            
    # Sort operations based on the number of candidate machines and processing time
    operations.sort(key=lambda x: (len(x[2][0]), min(x[2][1])))
    
    for job_id, op_num, op_data in operations:
        machines, times = op_data
        
        # Find the earliest possible start time for each machine
        available_times = {}
        for machine in machines:
            available_times[machine] = max(machine_available_time[machine], job_completion_time[job_id])
            
        # Choose the machine that allows the earliest completion time for the operation
        best_machine = min(available_times, key=available_times.get)
        processing_time = times[machines.index(best_machine)]
        start_time = available_times[best_machine]
        end_time = start_time + processing_time
        
        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        
        # Update schedule
        if job_id not in schedule:
            schedule[job_id] = []
            
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
    
    return schedule
