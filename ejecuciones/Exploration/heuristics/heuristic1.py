
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations with fewer machine options 
    and shorter processing times to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Create a list of operations with their attributes
    operations = []
    for job in jobs_data:
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            operations.append({
                'job': job,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times,
                'num_machines': len(machines)
            })
    
    # Sort operations based on the number of available machines (ascending) and processing time (ascending)
    operations.sort(key=lambda x: (x['num_machines'], min(x['times'])))
    
    for operation in operations:
        job = operation['job']
        op_num = operation['operation']
        machines = operation['machines']
        times = operation['times']
        
        best_machine = None
        min_end_time = float('inf')
        best_processing_time = None
        
        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + processing_time
            
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time
        
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
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
        
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
    
    return schedule
