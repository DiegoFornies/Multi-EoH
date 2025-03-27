
def heuristic(input_data):
    """Schedules jobs using a priority rule based on operation slack."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    # Calculate total work remaining for each job
    job_remaining_work = {}
    for job in range(1, n_jobs + 1):
        job_remaining_work[job] = sum(min(times) for machines, times in jobs[job])

    # Priority Queue for Operations (Slack-based)
    import heapq
    operation_queue = []
    for job in range(1, n_jobs + 1):
        heapq.heappush(operation_queue, (0, job, 0))  # (priority, job, op_idx)

    while operation_queue:
        priority, job, op_idx = heapq.heappop(operation_queue)
        operation = jobs[job][op_idx]
        machines, times = operation
        op_num = op_idx + 1

        best_machine = None
        min_finish_time = float('inf')

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            available_time = max(machine_available_time[machine], job_completion_time[job])
            finish_time = available_time + processing_time

            if finish_time < min_finish_time:
                min_finish_time = finish_time
                best_machine = machine
                best_start_time = available_time
                best_processing_time = processing_time

        if job not in schedule:
            schedule[job] = []
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job] = best_start_time + best_processing_time

        # Schedule the next operation for this job
        if op_idx + 1 < len(jobs[job]):
            # Calculate slack for the next operation and prioritize
            next_op_idx = op_idx + 1
            next_operation = jobs[job][next_op_idx]
            next_machines, next_times = next_operation
            min_next_time = min(next_times)
            slack = max(0, machine_available_time[best_machine] - job_completion_time[job])
            heapq.heappush(operation_queue, (slack, job, next_op_idx))
    return schedule
