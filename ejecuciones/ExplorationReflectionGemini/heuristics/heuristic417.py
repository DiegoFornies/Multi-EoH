
def heuristic(input_data):
    """Schedules operations using a priority queue based on earliest finish time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    import heapq

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    
    # Priority queue: (earliest_finish_time, job_id, operation_index, machine, processing_time)
    available_operations = []
    
    # Initialize available operations
    for job_id in range(1, n_jobs + 1):
        machines, times = jobs[job_id][0]
        min_time_index = times.index(min(times))
        machine = machines[min_time_index]
        processing_time = times[min_time_index]
        
        heapq.heappush(available_operations, (max(machine_available_times[machine], job_completion_times[job_id]) + processing_time, job_id, 0, machine, processing_time))
        
    while available_operations:
        finish_time, job_id, operation_index, machine, processing_time = heapq.heappop(available_operations)
        start_time = max(machine_available_times[machine], job_completion_times[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_times[machine] = end_time
        job_completion_times[job_id] = end_time

        # Add the next operation of the job to the priority queue
        next_operation_index = operation_index + 1
        if next_operation_index < len(jobs[job_id]):
            machines, times = jobs[job_id][next_operation_index]
            min_time_index = times.index(min(times))
            machine_next = machines[min_time_index]
            processing_time_next = times[min_time_index]
            heapq.heappush(available_operations, (max(machine_available_times[machine_next], job_completion_times[job_id]) + processing_time_next, job_id, next_operation_index, machine_next, processing_time_next))
            
    return schedule
