
def heuristic(input_data):
    """
    Heuristic scheduling algorithm for the FJSSP that attempts to minimize makespan.
    Prioritizes operations with fewer machine options and assigns to the earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Create a list of operations with their possible machines and times
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx + 1,
                'machines': machines,
                'times': times
            })
            
    # Sort operations by the number of possible machines (prioritize less flexible)
    operations.sort(key=lambda x: len(x['machines']))

    # Build the schedule
    for operation in operations:
        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']
        
        best_machine = None
        earliest_start_time = float('inf')
        best_processing_time = None
        
        # Find the machine that allows the earliest start time
        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time
                
        # Assign the operation to the best machine
        end_time = earliest_start_time + best_processing_time
        
        if job_id not in schedule:
            schedule[job_id] = []
        
        schedule[job_id].append({
            'Operation': op_idx,
            'Assigned Machine': best_machine,
            'Start Time': earliest_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
    
    return schedule
