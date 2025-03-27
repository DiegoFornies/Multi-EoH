
def heuristic(input_data):
    """Schedules jobs minimizing makespan & balancing machine load using an adaptive shortest processing time approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    operation_queue = []
    for job in range(1, n_jobs + 1):
        operation_queue.append((job, 0))

    while operation_queue:
        best_job, best_op_idx = None, None
        best_machine = None
        min_makespan = float('inf')

        for job, op_idx in operation_queue:
            machines, times = jobs[job][op_idx]
            
            for i, m in enumerate(machines):
                start_time = max(machine_time[m], job_completion_time[job])
                processing_time = times[i]
                makespan = start_time + processing_time
                
                if makespan < min_makespan:
                    min_makespan = makespan
                    best_job = job
                    best_op_idx = op_idx
                    best_machine = m
        
        job = best_job
        op_idx = best_op_idx
        m = best_machine
        machines, times = jobs[job][op_idx]
        processing_time = times[machines.index(m)]
        start = max(machine_time[m], job_completion_time[job])
        end = start + processing_time
        op_num = op_idx + 1

        schedule[job].append({'Operation': op_num, 'Assigned Machine': m, 'Start Time': start, 'End Time': end, 'Processing Time': processing_time})

        machine_time[m] = end
        job_completion_time[job] = end
        operation_queue.remove((job, op_idx))

        if op_idx + 1 < len(jobs[job]):
            operation_queue.append((job, op_idx + 1))

    return schedule
