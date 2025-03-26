
def heuristic(input_data):
    """Combines SPT and machine load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_operations_scheduled = {job: 0 for job in jobs}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        eligible_operations = []
        for job in jobs:
            op_idx = job_operations_scheduled[job]
            if op_idx < len(jobs[job]):
                eligible_operations.append((job, op_idx))

        if not eligible_operations:
            break

        best_op = None
        best_machine = None
        min_completion_time = float('inf')
        processing_time = None
        
        for job, op_idx in eligible_operations:
            machines, times = jobs[job][op_idx]

            for i, machine in enumerate(machines):
                start_time = max(job_completion_times[job], machine_load[machine])
                completion_time = start_time + times[i]
                
                #Heuristic objective function: prioritize lower completion time
                #Bias to balance machine load
                objective = completion_time + machine_load[machine]*0.01
                
                if objective < min_completion_time:
                    min_completion_time = objective
                    best_op = (job, op_idx)
                    best_machine = machine
                    processing_time = times[i]

        if best_op is not None:
            job, op_idx = best_op
            start_time = max(job_completion_times[job], machine_load[best_machine])
            end_time = start_time + processing_time
            op_num = op_idx + 1

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
