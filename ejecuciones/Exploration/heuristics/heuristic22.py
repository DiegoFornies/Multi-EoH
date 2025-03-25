
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes operations with the shortest processing time
    among available machines to minimize makespan and balance machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs_data}
    schedule = {job: [] for job in jobs_data}

    # Create a list of operations sorted by shortest processing time.
    eligible_operations = []
    for job_id, operations in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations):
            eligible_operations.append((job_id, op_idx, machines, times))

    #Sort operations by shortest processing time first, job number second and operation number third.
    eligible_operations.sort(key=lambda x: (min(x[3]), x[0], x[1]))

    while eligible_operations:
        #Select best operation
        job_id, op_idx, machines, times = eligible_operations.pop(0)
        
        # Find the machine that becomes available the soonest
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = times[m_idx]

        # Schedule the operation
        start_time = best_start_time
        end_time = start_time + best_processing_time
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        # Update machine and job completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        
    return schedule
