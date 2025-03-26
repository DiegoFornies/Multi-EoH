
def heuristic(input_data):
    """Prioritizes operations based on earliest due date (EDD)."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    job_remaining_operations = {j: list(range(len(jobs[j]))) for j in range(1, n_jobs + 1)}

    # Calculate due dates (simplified: sum of processing times)
    job_due_dates = {}
    for job_id in range(1, n_jobs + 1):
        due_date = 0
        for op_data in jobs[job_id]:
            due_date += min(op_data[1])
        job_due_dates[job_id] = due_date

    # Create a list of operations sorted by EDD.
    operation_queue = []
    for job_id in range(1, n_jobs + 1):
        for op_index in range(len(jobs[job_id])):
            operation_queue.append((job_id, op_index, job_due_dates[job_id]))

    operation_queue.sort(key=lambda x: x[2]) # Sort by job due date

    scheduled_operations = set()

    for job_id, operation_index, _ in operation_queue:
        if (job_id, operation_index) in scheduled_operations:
            continue

        if job_id not in schedule:
           schedule[job_id] = []

        operation_data = jobs[job_id][operation_index]
        possible_machines = operation_data[0]
        possible_times = operation_data[1]

        # Select machine with earliest available time among possible machines
        best_machine = None
        min_available_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(possible_machines):
            processing_time = possible_times[i]
            available_time = max(machine_available_times[machine], job_completion_times[job_id])

            if available_time < min_available_time:
                min_available_time = available_time
                best_machine = machine
                best_processing_time = processing_time

        start_time = min_available_time
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        scheduled_operations.add((job_id, operation_index))

    return schedule
