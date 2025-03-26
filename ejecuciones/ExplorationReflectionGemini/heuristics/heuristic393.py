
def heuristic(input_data):
    """Operation-centric, Earliest Due Date (EDD) with lookahead."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Calculate due dates based on remaining processing time for each job.
    job_due_dates = {}
    for job_id in range(1, n_jobs + 1):
        total_processing_time = 0
        for operation_data in jobs[job_id]:
            total_processing_time += min(operation_data[1])  # SPT for estimate
        job_due_dates[job_id] = total_processing_time

    # Operations queue: (job_id, operation_index)
    operations_queue = []
    for job_id in range(1, n_jobs + 1):
        operations_queue.append((job_id, 0))

    # Prioritize operations based on EDD of their respective jobs.
    operations_queue.sort(key=lambda x: job_due_dates[x[0]])

    while operations_queue:
        job_id, operation_index = operations_queue.pop(0)
        operation_data = jobs[job_id][operation_index]
        possible_machines = operation_data[0]
        possible_times = operation_data[1]

        # Find machine with earliest available time
        best_machine = None
        earliest_start_time = float('inf')
        best_processing_time = None

        for i in range(len(possible_machines)):
            machine = possible_machines[i]
            processing_time = possible_times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job_id])

            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        end_time = earliest_start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': earliest_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

        # Add next operation to the queue if it exists.
        if operation_index + 1 < len(jobs[job_id]):
            operations_queue.append((job_id, operation_index + 1))
            operations_queue.sort(key=lambda x: job_due_dates[x[0]])  # Re-sort

    return schedule
