
def heuristic(input_data):
    """
    Generates a schedule for the FJSSP using a shortest processing time (SPT) and earliest available machine (EAM) heuristic.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {job: [] for job in jobs}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}
    
    # Maintain a list of operations that are ready to be scheduled.
    ready_operations = []
    for job in jobs:
        ready_operations.append((job, 0))  # Initially, the first operation of each job is ready
    
    scheduled_operations = set()
    
    while ready_operations:
        # Find the operation with the shortest possible processing time among the ready operations.
        best_operation = None
        min_processing_time = float('inf')
        
        for job, op_idx in ready_operations:
            machines, times = jobs[job][op_idx]
            
            #Find the machine with minimum processing time and available time
            best_machine = None
            best_time = float('inf')
            
            for idx, machine in enumerate(machines):
                processing_time = times[idx]
                
                if processing_time < best_time:
                  best_time = processing_time
                  best_machine = machine
            
            if best_time < min_processing_time:
                min_processing_time = best_time
                best_operation = (job, op_idx, best_machine, best_time)
        
        job, op_idx, machine, processing_time = best_operation
        
        # Schedule the operation on the earliest available machine
        start_time = max(machine_available_time[machine], job_completion_time[job])
        end_time = start_time + processing_time
        
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        machine_available_time[machine] = end_time
        job_completion_time[job] = end_time
        
        # Remove the scheduled operation from the ready operations list
        ready_operations.remove((job, op_idx))
        
        # Add the next operation of the job to the ready operations list, if any
        if op_idx + 1 < len(jobs[job]):
            ready_operations.append((job, op_idx + 1))
            
    return schedule
