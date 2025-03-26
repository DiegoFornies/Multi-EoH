
def heuristic(input_data):
    """Prioritizes operations based on earliest due date."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    job_due_dates = {}

    # Estimate due dates based on total processing time
    for job_id in range(1, n_jobs + 1):
        total_processing_time = sum(min(times) for machines, times in jobs[job_id])
        job_due_dates[job_id] = total_processing_time * 1.5  # Simple due date estimation

    # Create a list of operations with job ID, operation index, and earliest start time
    operations = []
    for job_id in range(1, n_jobs + 1):
        for operation_index, operation_data in enumerate(jobs[job_id]):
            operations.append((job_id, operation_index))

    # Sort operations based on job due date
    operations.sort(key=lambda op: job_due_dates[op[0]])

    for job_id, operation_index in operations:
        operation_data = jobs[job_id][operation_index]
        possible_machines = operation_data[0]
        possible_times = operation_data[1]

        best_machine = None
        min_completion_time = float('inf')

        for machine in possible_machines:
            machine_index = possible_machines.index(machine)
            processing_time = possible_times[machine_index]

            start_time = max(machine_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            if end_time < min_completion_time:
                min_completion_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        machine_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job_id] = best_start_time + best_processing_time

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

    return schedule
