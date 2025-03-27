
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes operations based on shortest processing time on available machines.
    Greedily assigns operations to minimize makespan and balance machine load.
    """
    schedule = {}
    machine_available_time = {m: 0 for m in range(input_data['n_machines'])}
    job_completion_time = {j: 0 for j in range(1, input_data['n_jobs'] + 1)}  # Completion time of each job
    operation_queue = []

    # Initialize operation_queue with all first operations
    for job_id in range(1, input_data['n_jobs'] + 1):
        operation_queue.append((job_id, 0)) # job_id, operation index within job

    while operation_queue:
        # Find the operation with the shortest processing time among all schedulable operations
        best_operation = None
        min_processing_time = float('inf')

        for job_id, op_idx in operation_queue:
            machines, times = input_data['jobs'][job_id][op_idx]
            
            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                if processing_time < min_processing_time:
                    min_processing_time = processing_time
                    best_operation = (job_id, op_idx, machine, processing_time)

        job_id, op_idx, machine, processing_time = best_operation
        machines, times = input_data['jobs'][job_id][op_idx]

        # Determine start time
        start_time = max(machine_available_time[machine], job_completion_time[job_id])

        # Schedule the operation
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []
        
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[machine] = end_time
        job_completion_time[job_id] = end_time
        
        # Remove current operation from the queue
        operation_queue.remove((job_id, op_idx))

        # Add the next operation of the job to the queue, if any
        if op_idx + 1 < len(input_data['jobs'][job_id]):
            operation_queue.append((job_id, op_idx + 1))

    return schedule
