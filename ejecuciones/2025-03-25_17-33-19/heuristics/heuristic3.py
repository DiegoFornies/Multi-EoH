
def heuristic(input_data):
    """
    A heuristic to schedule jobs, minimizing makespan by prioritizing
    operations based on processing time and machine availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    
    schedule = {j: [] for j in jobs}
    
    unscheduled_operations = {}
    for job_id, operations in jobs.items():
        unscheduled_operations[job_id] = list(range(len(operations)))

    while any(unscheduled_operations.values()):
        eligible_operations = []
        for job_id, operations_indices in unscheduled_operations.items():
            if operations_indices:
                op_index = operations_indices[0]
                machines, times = jobs[job_id][op_index]
                eligible_operations.append((job_id, op_index, machines, times))

        if not eligible_operations:
            break

        best_operation = None
        min_end_time = float('inf')

        for job_id, op_index, machines, times in eligible_operations:
            
            best_machine, min_machine_end_time = None, float('inf')
            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + times[m_idx]
                if end_time < min_machine_end_time:
                    min_machine_end_time = end_time
                    best_machine = machine
                    best_processing_time = times[m_idx]

            if min_machine_end_time < min_end_time:
                min_end_time = min_machine_end_time
                best_operation = (job_id, op_index, best_machine, best_processing_time, min_machine_end_time - best_processing_time) #include the start time.
                
        job_id, op_index, assigned_machine, processing_time, start_time = best_operation
        end_time = start_time + processing_time
            
        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
            
        machine_available_time[assigned_machine] = end_time
        job_completion_time[job_id] = end_time
            
        unscheduled_operations[job_id].pop(0)
    
    return schedule
