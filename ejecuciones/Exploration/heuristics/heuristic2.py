
def heuristic(input_data):
    """
    Schedules jobs using a shortest processing time (SPT) and earliest available machine (EAM) heuristic.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Sort operations by processing time, prioritizing shorter operations
    operation_queue = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            min_time_idx = times.index(min(times))  # Choose the shortest time option
            operation_queue.append((times[min_time_idx], job_id, op_idx, machines, times))
    
    operation_queue.sort()  # Sort by shortest processing time

    for _, job_id, op_idx, machines, times in operation_queue:
        if job_id not in schedule:
            schedule[job_id] = []
        
        # Find earliest available machine for the operation
        best_machine, best_start_time, best_processing_time = None, float('inf'), float('inf')
        
        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        start_time = best_start_time
        machine = best_machine
        processing_time = best_processing_time

        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_times[machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
