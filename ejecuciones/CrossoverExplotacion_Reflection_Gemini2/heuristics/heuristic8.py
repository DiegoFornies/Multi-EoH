
def heuristic(input_data):
    """
    A heuristic for the FJSSP that aims to minimize makespan by considering
    machine availability and operation durations.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    # Prioritize operations based on SPT (Shortest Processing Time)
    operation_queue = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            min_time_index = times.index(min(times))
            operation_queue.append((times[min_time_index], job_id, op_idx)) # (Processing Time, Job ID, Operation Index)
    
    operation_queue.sort() # Sort by shortest processing time

    for processing_time, job_id, op_idx in operation_queue:
        machines, times = jobs[job_id][op_idx]
        
        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = times[m_idx]
        
        start_time = best_start_time
        end_time = start_time + best_processing_time
        
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
