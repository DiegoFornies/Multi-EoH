
def heuristic(input_data):
    """Minimize makespan using a shortest processing time-based heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}
    
    op_queue = []
    for job in jobs:
        op_queue.append((job, 0))
    
    while op_queue:
        
        best_job = None
        best_machine = None
        min_end_time = float('inf')
        
        for job, op_idx in op_queue:
            machines, times = jobs[job][op_idx]
            for m, t in zip(machines, times):
                start_time = max(machine_time[m], job_completion_time[job])
                end_time = start_time + t
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_job = job
                    best_machine = m
                    best_time = t
                    
        if best_job is None:
            break

        op_idx = job_ops[best_job]

        if best_job not in schedule:
            schedule[best_job] = []

        start_time = max(machine_time[best_machine], job_completion_time[best_job])
        end_time = start_time + best_time

        schedule[best_job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })
        
        machine_time[best_machine] = end_time
        job_completion_time[best_job] = end_time
        job_ops[best_job] += 1
        
        op_queue.remove((best_job, op_idx))
        
        if job_ops[best_job] < len(jobs[best_job]):
            op_queue.append((best_job, job_ops[best_job]))

    return schedule
