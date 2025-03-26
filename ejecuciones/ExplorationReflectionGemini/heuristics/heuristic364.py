
def heuristic(input_data):
    """Schedules jobs using a combined SPT and load balancing heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    available_operations = []
    for job_id in jobs:
        available_operations.append((job_id, 0))

    while available_operations:
        best_op = None
        best_score = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]
            
            for i, machine in enumerate(machines):
                start_time = max(job_completion_times[job_id], machine_load[machine])
                end_time = start_time + times[i]
                score = 0.6 * end_time + 0.4 * machine_load[machine] # Combined score
                
                if score < best_score:
                    best_score = score
                    best_op = (job_id, op_idx, machine, times[i], start_time, end_time)
        
        job_id, op_idx, assigned_machine, processing_time, start_time, end_time = best_op
        op_num = op_idx + 1

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        machine_load[assigned_machine] = end_time
        job_completion_times[job_id] = end_time
        available_operations.remove((job_id, op_idx))

        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))
            
    return schedule
