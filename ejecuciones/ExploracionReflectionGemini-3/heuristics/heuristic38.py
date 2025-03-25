
def heuristic(input_data):
    """
    A heuristic to schedule jobs by prioritizing operations with shorter processing times and machines with less workload.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    
    # Collect all operations and their details
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append({
                'job': job,
                'op_idx': op_idx,
                'machines': machines,
                'times': times,
                'op_num': op_idx + 1
            })
    
    # Sort operations by shortest processing time
    operations.sort(key=lambda op: min(op['times']))
    
    for op in operations:
        job = op['job']
        op_idx = op['op_idx']
        machines = op['machines']
        times = op['times']
        op_num = op['op_num']
        
        # Find the best machine based on availability and processing time
        best_machine = None
        min_end_time = float('inf')
        
        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_load[machine], job_completion_times[job])
            end_time = start_time + processing_time
            
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time
        
        # Schedule the operation
        start_time = max(machine_load[best_machine], job_completion_times[job])
        end_time = start_time + best_processing_time
        
        if job not in schedule:
            schedule[job] = []
        
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        # Update machine load and job completion time
        machine_load[best_machine] = end_time
        job_completion_times[job] = end_time
    
    return schedule
