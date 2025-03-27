
def heuristic(input_data):
    """Heuristic for FJSSP minimizing makespan, idle time, and balancing load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize schedule and machine availability
    schedule = {}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}

    # Prioritize operations based on shortest processing time
    operation_queue = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            operation_queue.append((job_id, op_idx, machines, times))

    # Sort operations by shortest processing time amongst available machines
    operation_queue.sort(key=lambda x: min(x[3]))

    # Schedule operations one by one
    for job_id, op_idx, machines, times in operation_queue:
        # Find the earliest available machine and time slot
        best_machine, start_time, processing_time = None, float('inf'), None
        
        for m_idx, machine in enumerate(machines):
            available_time = max(machine_availability[machine], job_completion_times[job_id])
            if available_time < start_time:
                best_machine, start_time, processing_time = machine, available_time, times[m_idx]

        if best_machine is None:
            # No eligible machine found, choose the first one.
            best_machine = machines[0]
            start_time = max(machine_availability[best_machine], job_completion_times[job_id])
            processing_time = times[0]

        # Update schedule and machine availability
        if job_id not in schedule:
            schedule[job_id] = []
        
        end_time = start_time + processing_time
        
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        machine_availability[best_machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
