
def heuristic(input_data):
    """A heuristic for FJSSP scheduling that considers machine availability and job completion time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    # Initialize schedule and machine availability
    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(1, n_machines + 1)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    
    # List of operations
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))
            
    # Sort operations by the shortest processing time
    operations.sort(key=lambda x: min(x[3]))
    
    for job, op_num, machines, times in operations:
        # Find the earliest available machine for the job operation
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        
        for i, machine in enumerate(machines):
            processing_time = times[i]
            available_time = machine_available_time[machine]
            start_time = max(available_time, job_completion_time[job])
            
            if start_time < best_start_time:
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time
                
        # Schedule the operation on the best machine
        end_time = best_start_time + best_processing_time
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
