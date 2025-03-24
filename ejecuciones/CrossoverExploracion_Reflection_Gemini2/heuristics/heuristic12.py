
def heuristic(input_data):
    """A heuristic for FJSSP aiming for makespan and balance."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}  # Store the schedule for each job
    machine_available_time = {m: 0 for m in range(n_machines)}  # Track when each machine is available
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Track when each job can start its next operation
    machine_load = {m: 0 for m in range(n_machines)} # Track total load on machines

    # Prioritize jobs based on the total processing time required
    job_priority = sorted(jobs.keys(), key=lambda job_id: sum(min(times) for machines, times in jobs[job_id]), reverse=True) #Longest processing time first
    
    for job in job_priority:
        schedule[job] = []
        current_time = 0
        
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1
            best_machine = -1
            best_start_time = float('inf')
            best_processing_time = -1

            # Find the best machine for the current operation
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                
                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Assign the operation to the best machine
            start_time = best_start_time
            end_time = start_time + best_processing_time
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability and job completion time
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time
            machine_load[best_machine] += best_processing_time

    return schedule
