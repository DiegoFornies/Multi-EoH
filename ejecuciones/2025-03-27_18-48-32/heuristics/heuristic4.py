
def heuristic(input_data):
    """
    A scheduling heuristic that prioritizes shortest processing time (SPT) and machine load balancing.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))
    
    # Sort operations by shortest processing time first.
    operations.sort(key=lambda x: min(x[3]))

    for job, op_num, machines, times in operations:
        best_machine, best_time = None, float('inf')
        
        # Find the machine with the shortest available time
        for i, m in enumerate(machines):
            start_time = max(machine_load[m], job_completion_times[job])
            
            if start_time + times[i] < best_time:
                best_machine, best_time = m, start_time + times[i]
                processing_time = times[i]

        start_time = max(machine_load[best_machine], job_completion_times[job])
        end_time = start_time + processing_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_load[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
