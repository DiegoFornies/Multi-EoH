
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes jobs with shorter total processing time and operations
    with fewer machine options to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Calculate total processing time for each job
    job_processing_times = {}
    for job, ops in jobs_data.items():
        total_time = sum(min(times) for machines, times in ops)  # Consider shortest time for each op
        job_processing_times[job] = total_time

    # Sort jobs by total processing time (shortest first)
    sorted_jobs = sorted(job_processing_times.items(), key=lambda item: item[1])
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data.keys()} # Initialize job completion times

    for job, _ in sorted_jobs:
        schedule[job] = []
        
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1

            # Prioritize machines based on availability and fewest options
            available_machines = [(m, times[i]) for i, m in enumerate(machines)]
            
            # Sort machines by earliest available time
            machine_times = [(m, machine_available_time[m]) for m, _ in available_machines]
            machine_times.sort(key=lambda x: x[1])
            
            best_machine = machine_times[0][0]
            processing_time = next(t for m,t in available_machines if m == best_machine)

            # Schedule the operation on the selected machine
            start_time = max(machine_available_time[best_machine], job_completion_time[job])
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
            job_completion_time[job] = end_time  #Next operation of this job must start after this operation
            
    return schedule
