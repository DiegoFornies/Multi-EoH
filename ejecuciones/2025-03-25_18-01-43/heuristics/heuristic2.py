
def heuristic(input_data):
    """
    Heuristic to solve FJSSP prioritizing operations with fewer machine options
    and using a earliest start time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    schedule = {job: [] for job in range(1, n_jobs + 1)}
    
    # Create a list of all operations, including job and operation number
    all_operations = []
    for job in jobs_data:
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            all_operations.append((job, op_idx + 1, machines, times))

    # Sort operations by the number of available machines (fewest first)
    all_operations.sort(key=lambda x: len(x[2]))

    for job, op_num, machines, times in all_operations:
        # Find the earliest possible start time for this operation
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_times[machine], job_completion_times[job])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time
        
        # Schedule the operation on the chosen machine at the earliest start time
        end_time = best_start_time + best_processing_time
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine available time and job completion time
        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time
    
    return schedule
