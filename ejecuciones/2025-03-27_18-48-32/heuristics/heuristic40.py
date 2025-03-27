
def heuristic(input_data):
    """
    Prioritizes operations with the shortest processing time on least loaded machine, balancing makespan and machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}  # Tracks when each machine is available
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}  # Tracks completion time of each job
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}
    machine_loads = {m: 0 for m in range(n_machines)}  # Tracks total load on each machine

    # Store operations with their potential start times across machines
    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 1)) # Add job and operation number 1
        
    while eligible_operations:
        # Find the operation that can start earliest among eligible ones
        best_op = None
        earliest_start = float('inf')
        best_machine = None
        best_time = None
        best_job = None
        
        # Iterates through eligible operations to find earliest start time
        for job, op_num in eligible_operations:
            machines, times = jobs_data[job][op_num - 1]
            
            # Find best machine and processing time
            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_times[job])
                
                # Prioritize machines with lower current load
                weighted_start_time = start_time + machine_loads[m] 
                
                if weighted_start_time < earliest_start:
                    earliest_start = weighted_start_time
                    best_op = op_num
                    best_machine = m
                    best_time = times[m_idx]
                    best_job = job
        
        # Schedules the best_op
        start_time = max(machine_available_times[best_machine], job_completion_times[best_job])
        end_time = start_time + best_time
        scheduled_operations[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })
        
        # Updates completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[best_job] = end_time
        machine_loads[best_machine] += best_time
        
        eligible_operations.remove((best_job, best_op))
        
        # Add new eligible operations
        if best_op < len(jobs_data[best_job]):
            eligible_operations.append((best_job, best_op + 1))

    return scheduled_operations
