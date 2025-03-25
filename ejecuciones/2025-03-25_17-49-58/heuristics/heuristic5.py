
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes operations with fewer machine options."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Create a list of operations with job and operation indices
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))
    
    # Sort operations based on the number of available machines
    operations.sort(key=lambda x: len(x[2]))
    
    for job, op_num, machines, times in operations:
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        
        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            available_time = machine_available_time[machine]
            start_time = max(available_time, job_completion_time[job])
            
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time
        
        if job not in schedule:
            schedule[job] = []
        
        end_time = best_start_time + best_processing_time
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
