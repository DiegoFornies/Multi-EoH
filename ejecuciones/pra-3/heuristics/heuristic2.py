
def heuristic(input_data):
    """Schedules jobs minimizing makespan by prioritizing operations with shorter processing times and considering machine availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    
    # List of operations: (job_id, operation_index, machines, times)
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx, machines, times))
            
    # Sort operations by shortest processing time, considering all machines.
    operations.sort(key=lambda op: min(op[3]))  # Sort by minimum possible processing time
    
    for job_id, op_idx, machines, times in operations:
        op_num = op_idx + 1
        
        # Find the machine and time that minimizes completion time.
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        
        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            
            if start_time + times[m_idx] < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = times[m_idx]
                
        # Assign the operation to the best machine found.
        end_time = best_start_time + best_processing_time
        
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        # Update machine availability and job completion time.
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
