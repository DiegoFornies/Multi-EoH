
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes jobs with fewer remaining operations
    and selects the machine with the earliest available time for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_current_op = {job: 0 for job in jobs_data}
    job_last_end_time = {job: 0 for job in jobs_data}
    remaining_ops = {job: len(jobs_data[job]) for job in jobs_data}

    scheduled_operations = 0
    total_operations = sum(len(ops) for ops in jobs_data.values())
    
    while scheduled_operations < total_operations:
        eligible_jobs = [job for job in jobs_data if job_current_op[job] < len(jobs_data[job])]

        if not eligible_jobs:
            break

        # Prioritize jobs with fewer remaining operations
        job_priorities = {job: remaining_ops[job] for job in eligible_jobs}
        sorted_jobs = sorted(eligible_jobs, key=lambda job: job_priorities[job])
        
        for job in sorted_jobs:
            op_idx = job_current_op[job]
            machines, times = jobs_data[job][op_idx]
            
            # Find the machine with the earliest available time
            best_machine, best_time = None, float('inf')
            for i, machine in enumerate(machines):
                available_time = max(machine_available_time[machine], job_last_end_time[job])
                if available_time < best_time:
                    best_time = available_time
                    best_machine = machine
                    processing_time = times[i]
                    
            if best_machine is not None:
                start_time = best_time
                end_time = start_time + processing_time
                
                if job not in schedule:
                    schedule[job] = []
                
                schedule[job].append({
                    'Operation': op_idx + 1,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })
                
                machine_available_time[best_machine] = end_time
                job_last_end_time[job] = end_time
                job_current_op[job] += 1
                remaining_ops[job] -= 1
                scheduled_operations += 1
            
            if remaining_ops[job] == 0:
                continue # No need to check this job again this iteration

    return schedule
