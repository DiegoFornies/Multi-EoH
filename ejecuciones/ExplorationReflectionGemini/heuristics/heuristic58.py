
def heuristic(input_data):
    """Schedules jobs prioritizing shortest processing time across all jobs."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    
    operations = []
    for job in range(1, n_jobs + 1):
        for op_idx, (machines, times) in enumerate(jobs[job]):
            min_time = min(times)
            operations.append((min_time, job, op_idx, machines, times))

    operations.sort()

    for min_time, job, op_idx, machines, times in operations:
        op_num = op_idx + 1
        
        best_machine = None
        min_completion_time = float('inf')
        best_processing_time = None
        best_start_time = None
        
        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_time[machine], job_completion_time[job])
            completion_time = start_time + processing_time
            
            if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = machine
                best_processing_time = processing_time
                best_start_time = start_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': min_completion_time,
            'Processing Time': best_processing_time
        })
        
        machine_time[best_machine] = min_completion_time
        job_completion_time[job] = min_completion_time

    return schedule
