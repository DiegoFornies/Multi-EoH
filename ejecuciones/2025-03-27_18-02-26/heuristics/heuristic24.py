
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes balancing machine load and reducing job idle time."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}  # Earliest available time for each machine
    machine_load = {m: 0 for m in range(n_machines)}  # Total processing time assigned to each machine

    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)} # last operation time for the job
    
    eligible_operations = {}
    for job in range(1, n_jobs + 1):
        eligible_operations[job] = 1 # first operation for each job

    
    scheduled_operations = 0
    total_operations = sum(len(ops) for ops in jobs.values())
    
    while scheduled_operations < total_operations:

        best_op, best_machine, best_start_time, best_processing_time = None, None, float('inf'), None
        
        # Find the best eligible operation across all jobs
        for job in range(1, n_jobs + 1):
            if job not in jobs: continue # in case of missing job number in the input data

            if eligible_operations[job] <= len(jobs[job]):
                op_idx = eligible_operations[job] - 1
                machines, times = jobs[job][op_idx]
                
                # Evaluate each possible machine for the current operation
                for m_idx, machine in enumerate(machines):
                    processing_time = times[m_idx]
                    start_time = max(machine_time[machine], job_completion_time[job]) # Ensure both machine and job are ready

                    # Prioritize lower machine load and earlier start time
                    if start_time + processing_time < best_start_time:
                        best_op = (job, op_idx + 1) # job and the operation number
                        best_machine = machine
                        best_start_time = start_time
                        best_processing_time = processing_time
                
        # Schedule the best operation
        if best_op:
            job, op_num = best_op
            
            if job not in schedule:
                schedule[job] = []

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })
            
            machine_time[best_machine] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_time[job] = best_start_time + best_processing_time
            
            eligible_operations[job] += 1
            scheduled_operations += 1
        else:
            break # No eligible operations found (possibly an issue with the input data)
    
    return schedule
