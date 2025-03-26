
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) that considers
    minimizing idle time and balancing machine load by prioritizing
    operations based on the shortest processing time and machine availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}

    # Create a list of all operations with their possible machines and processing times.
    # Prioritize based on shortest processing time
    all_operations = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            all_operations.append({
                'job_id': job_id,
                'op_idx': op_idx,
                'machines': machines,
                'times': times
            })

    def sorting_key(op):
        return min(op['times'])

    all_operations.sort(key=sorting_key)

    while all_operations:
        # Select the next operation
        operation = all_operations.pop(0)
        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        # Find the best machine to assign the operation to: minimize idle time and machine load
        best_machine = None
        min_end_time = float('inf')
        
        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time
                best_start_time = start_time

        # Assign the operation to the chosen machine
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })
        
        # Update machine availability and job completion time
        machine_available_times[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time

    return schedule
