
def heuristic(input_data):
    """
    Combines min workload & earliest avail time for FJSSP scheduling.
    Prioritizes machines with less workload and earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}  # Machine workload
    machine_available_time = {m: 0 for m in range(n_machines)} # Machine availability
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)} # Job completion
    
    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            # Find the best machine
            best_machine = None
            min_combined_score = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time
                
                # Combine workload and availability.  Normalize processing time.
                combined_score = machine_load[machine] + end_time  # Try both
                # Smaller combined score = better

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_load[best_machine] = best_start_time + best_processing_time # update workload
            machine_available_time[best_machine] = best_start_time + best_processing_time # update availability
            job_completion_time[job] = best_start_time + best_processing_time # update job complete

    return schedule
