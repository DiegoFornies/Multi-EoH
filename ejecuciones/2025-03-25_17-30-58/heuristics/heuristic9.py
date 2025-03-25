
def heuristic(input_data):
    """A heuristic for FJSSP that minimizes makespan and balances machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Priority queue for operations, sorted by shortest processing time on any machine.
    import heapq
    operation_queue = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            min_time = min(times)
            heapq.heappush(operation_queue, (min_time, job_id, op_idx))

    while operation_queue:
        _, job_id, op_idx = heapq.heappop(operation_queue)
        machines, times = jobs[job_id][op_idx]

        # Find the machine that allows the earliest completion time.
        best_machine = None
        earliest_completion = float('inf')
        best_processing_time = None

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            completion_time = start_time + processing_time

            if completion_time < earliest_completion:
                earliest_completion = completion_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the best machine.
        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine available time and job completion time.
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

        # Add the next operation for this job to the queue if it exists.
        next_op_idx = op_idx + 1
        if next_op_idx < len(jobs[job_id]):
            next_machines, next_times = jobs[job_id][next_op_idx]
            next_min_time = min(next_times)
            heapq.heappush(operation_queue, (next_min_time, job_id, next_op_idx))

    return schedule
