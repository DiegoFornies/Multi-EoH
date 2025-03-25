
def heuristic(input_data):
    """Aims to minimize makespan and idle time by prioritizing operations based on shortest processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Flatten operations into a list for scheduling
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job': job_id,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times
            })
    
    # Sort operations by shortest processing time on the first available machine
    operations.sort(key=lambda op: min(op['times']))

    for op in operations:
        job_id = op['job']
        op_num = op['operation']
        machines = op['machines']
        times = op['times']

        best_machine = None
        min_end_time = float('inf')
        processing_time = None

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + times[i]

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = times[i]
        
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time
        
        if job_id not in schedule:
            schedule[job_id] = []
        
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
