
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP).
    Prioritizes operations based on shortest processing time on available machines
    while respecting operation, machine, and sequence constraints.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    # Initialize schedule and machine availability
    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of operations that need scheduling
    operations_to_schedule = []
    for job_id, operations in jobs_data.items():
        for op_idx, op_data in enumerate(operations):
            operations_to_schedule.append((job_id, op_idx, op_data))

    # Sort operations by shortest processing time
    operations_to_schedule.sort(key=lambda x: min(x[2][1]))

    # Iterate through operations and schedule them
    for job_id, op_idx, op_data in operations_to_schedule:
        machines, times = op_data

        # Find the machine with the earliest available time
        best_machine = None
        min_start_time = float('inf')
        processing_time = None
        
        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                processing_time = times[m_idx]
                

        # Schedule the operation on the chosen machine
        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine availability and job completion time
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
