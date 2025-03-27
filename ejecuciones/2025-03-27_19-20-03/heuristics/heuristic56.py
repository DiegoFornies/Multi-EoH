
def heuristic(input_data):
    """Schedules jobs using a global makespan minimization approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Prioritize operations based on the earliest possible end time.
    operations = []
    for job in jobs:
        for op_idx, (machines, times) in enumerate(jobs[job]):
            for m_idx, machine in enumerate(machines):
                start_time = max(machine_time[machine], job_completion_time[job])
                end_time = start_time + times[m_idx]
                operations.append((end_time, job, op_idx, machine, times[m_idx]))
    
    operations.sort()  # Sort by earliest possible end time

    for end_time, job, op_idx, machine, processing_time in operations:
        if job not in schedule:
            schedule[job] = []
        
        start_time = max(machine_time[machine], job_completion_time[job])

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': start_time + processing_time,
            'Processing Time': processing_time
        })
        
        machine_time[machine] = start_time + processing_time
        job_completion_time[job] = start_time + processing_time

    return schedule
