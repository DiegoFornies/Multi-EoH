
def heuristic(input_data):
    """Combines shortest processing time and least loaded machine for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    
    job_total_processing_times = {}
    for job, operations in jobs.items():
        total_time = 0
        for machines, times in operations:
            total_time += min(times)
        job_total_processing_times[job] = total_time

    available_jobs = sorted(list(jobs.keys()), key=lambda x: job_total_processing_times[x])
    job_operations_scheduled = {job: 0 for job in jobs}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        for job in list(jobs.keys()):
            next_op_index = job_operations_scheduled[job]

            if next_op_index >= len(jobs[job]):
                continue
            
            machines, times = jobs[job][next_op_index]
            op_num = next_op_index + 1
            
            best_machine = None
            best_time = float('inf')
            processing_time = None

            for i, m in enumerate(machines):
                available_time = machine_load[m]
                start_time = max(job_completion_times[job], available_time)
                if start_time < best_time:
                    best_time = start_time
                    best_machine = m
                    processing_time = times[i]
            
            if best_machine is not None:
                start_time = max(job_completion_times[job], machine_load[best_machine])
                end_time = start_time + processing_time

                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })
                
                machine_load[best_machine] = end_time
                job_completion_times[job] = end_time
                job_operations_scheduled[job] += 1

    return schedule
