
def heuristic(input_data):
    """
    Schedules jobs considering machine availability and job dependencies,
    prioritizing shorter operations and machines with lower utilization
    to minimize makespan.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}  # Track when each job finishes its last operation
    schedule = {}

    # Create a priority queue of operations, sorted by shortest processing time
    import heapq
    operation_queue = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            # Use the shortest processing time as the initial priority
            shortest_time = min(times)
            heapq.heappush(operation_queue, (shortest_time, job_id, op_idx))  # (priority, job_id, op_idx)

    while operation_queue:
        _, job_id, op_idx = heapq.heappop(operation_queue)
        machines, times = jobs[job_id][op_idx]

        # Find the earliest available machine for the operation
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]

            # Job's prior operation completion time
            job_ready_time = job_completion_times[job_id] if op_idx > 0 else 0

            # Earliest time machine is available
            machine_ready_time = machine_available_times[machine]

            start_time = max(job_ready_time, machine_ready_time)

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the selected machine
        end_time = best_start_time + best_processing_time
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

        # Add the next operation of the job to the queue if it exists
        next_op_idx = op_idx + 1
        if next_op_idx < len(jobs[job_id]):
            next_machines, next_times = jobs[job_id][next_op_idx]
            shortest_next_time = min(next_times)
            heapq.heappush(operation_queue, (shortest_next_time, job_id, next_op_idx))

    return schedule
