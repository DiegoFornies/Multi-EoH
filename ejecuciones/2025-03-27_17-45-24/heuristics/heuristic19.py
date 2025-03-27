
def heuristic(input_data):
    """
    Heuristic for FJSSP minimizing makespan by earliest start time.

    Prioritizes operations with the fewest feasible machines.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize schedule, machine availability, and operation readiness
    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    operation_queue = []

    # Populate initial operation queue
    for job, operations in jobs_data.items():
        operation_queue.append((job, 0))  # (job, operation_index)

    # Define a key function for sorting operations
    def operation_priority(item):
        job, op_idx = item
        machines, _ = jobs_data[job][op_idx]
        return len(machines)

    # Main scheduling loop
    while operation_queue:
        # Sort the operation queue based on operation_priority,
        # prioritize operation with the fewest machines that can process it.
        operation_queue.sort(key=operation_priority)
        job, op_idx = operation_queue.pop(0)
        
        machines, times = jobs_data[job][op_idx]
        
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        
        # find the machine to minimize makespan
        for machine, time in zip(machines, times):
            start_time = max(machine_availability[machine], job_completion_times[job])
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = time

        # Schedule the operation
        start_time = best_start_time
        end_time = start_time + best_processing_time
        machine = best_machine

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        # Update machine availability and job completion time
        machine_availability[machine] = end_time
        job_completion_times[job] = end_time

        # Add the next operation of the job to the queue, if it exists
        if op_idx + 1 < len(jobs_data[job]):
            operation_queue.append((job, op_idx + 1))

    return schedule
