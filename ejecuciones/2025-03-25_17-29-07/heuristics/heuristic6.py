
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations based on the shortest processing time available.
    It iterates through jobs and operations, assigning to the machine with the earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    
    # Flatten operations with job and operation indices
    flattened_operations = []
    for job_id, operations in jobs_data.items():
        for op_idx, op_data in enumerate(operations):
            flattened_operations.append((job_id, op_idx + 1, op_data))
            
    # Sort operations based on shortest processing time first available
    flattened_operations.sort(key=lambda x: min(x[2][1]))

    for job_id, op_num, op_data in flattened_operations:
        machines, times = op_data
        
        # Find the earliest available time slot for the operation
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = times[m_idx]
                
        # Schedule the operation on the selected machine
        end_time = best_start_time + best_processing_time
        
        # Update machine and job completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

        # Update schedule
        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

    return schedule
