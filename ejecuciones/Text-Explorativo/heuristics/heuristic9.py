
def heuristic(input_data):
    """Schedules jobs using a machine load balancing heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    schedule = {job: [] for job in range(1, n_jobs + 1)}

    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations based on the number of available machines
    operations.sort(key=lambda x: len(x[2]))

    for job, op_num, machines, times in operations:
        # Find the machine with the earliest available time among feasible machines
        best_machine = None
        min_end_time = float('inf')
        
        for i, machine in enumerate(machines):
            available_time = machine_available_times[machine]
            start_time = max(available_time, job_completion_times[job])
            end_time = start_time + times[i]
            
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = times[i]
                start = start_time
        
        if best_machine is None:
            # If no suitable machine is found (shouldn't happen with valid input), use a fallback
            best_machine = machines[0]
            processing_time = times[0]
            start = max(machine_available_times[best_machine], job_completion_times[job])
            min_end_time = start + processing_time
            
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start,
            'End Time': min_end_time,
            'Processing Time': processing_time
        })
        
        machine_available_times[best_machine] = min_end_time
        job_completion_times[job] = min_end_time
    
    return schedule
