
def heuristic(input_data):
    """
    A scheduling heuristic that prioritizes jobs with fewer remaining operations
    and machines with lower utilization to minimize makespan and balance machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_current_op = {job: 0 for job in jobs_data}
    job_last_end_time = {job: 0 for job in jobs_data}
    job_remaining_ops = {job: len(jobs_data[job]) for job in jobs_data}
    
    scheduled_operations = 0
    total_operations = sum(len(ops) for ops in jobs_data.values())

    while scheduled_operations < total_operations:
        eligible_operations = []
        for job in jobs_data:
            if job_current_op[job] < len(jobs_data[job]):
                eligible_operations.append(job)
        
        if not eligible_operations:
            break 

        # Prioritize jobs with fewer remaining operations
        eligible_operations.sort(key=lambda job: job_remaining_ops[job])

        best_job, best_machine, best_start_time, best_processing_time = None, None, float('inf'), None
        
        for job in eligible_operations:
            op_idx = job_current_op[job]
            machines, times = jobs_data[job][op_idx]
            
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_last_end_time[job])

                if start_time < best_start_time:
                    best_job = job
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        if best_job is not None:
            op_idx = job_current_op[best_job]
            op_num = op_idx + 1
            end_time = best_start_time + best_processing_time
            
            if best_job not in schedule:
                schedule[best_job] = []

            schedule[best_job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })
            
            machine_available_time[best_machine] = end_time
            job_last_end_time[best_job] = end_time
            job_current_op[best_job] += 1
            job_remaining_ops[best_job] -= 1
            scheduled_operations += 1
    
    return schedule
