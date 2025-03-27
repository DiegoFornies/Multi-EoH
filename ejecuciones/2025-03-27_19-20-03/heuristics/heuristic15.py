
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes operations based on shortest processing time
    and assigns them to the earliest available machine to minimize makespan and balance machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)} # Initialize job completion times
    
    # Create a list of operations with job, operation index, and machine options
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations by shortest processing time across all possible machines
    operations.sort(key=lambda x: min(x[3]))  # Sort by minimum processing time
    
    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1
        
        # Find the machine with the earliest available time for this operation
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job]) # Consider both machine and job availabilities

            if start_time < best_start_time:
                best_machine = machine
                best_start_time = start_time
                best_processing_time = times[m_idx]
        
        # Schedule the operation on the best machine
        end_time = best_start_time + best_processing_time

        if job not in schedule:
            schedule[job] = []
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
