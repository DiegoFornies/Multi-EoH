
def heuristic(input_data):
    """
    A simple heuristic to solve the FJSSP problem. Prioritizes jobs with fewer operations,
    and assigns operations to the machine that becomes available earliest among feasible options.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    
    # Sort jobs by number of remaining operations (shortest job first)
    job_order = sorted(jobs_data.keys(), key=lambda job: len(jobs_data[job]))
    
    for job in job_order:
        schedule[job] = []
        current_time = job_completion_time[job]
        
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1
            best_machine, best_time = None, float('inf')
            
            # Find the machine with the earliest available time among feasible options
            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                available_time = max(machine_available_time[machine], current_time)
                
                if available_time < best_time:
                    best_time = available_time
                    best_machine = machine
                    best_processing_time = processing_time
            
            start_time = best_time
            end_time = start_time + best_processing_time
            
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })
            
            machine_available_time[best_machine] = end_time
            current_time = end_time
            job_completion_time[job] = current_time
            
    return schedule
