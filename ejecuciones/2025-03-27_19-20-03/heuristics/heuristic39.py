
def heuristic(input_data):
    """Schedules operations based on shortest processing time first."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of all operations with job and op indices
    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx))

    # Sort operations by shortest processing time on any machine
    operations.sort(key=lambda x: min(input_data['jobs'][x[0]][x[1]][1]))

    for job_id, op_idx in operations:
        operation = jobs[job_id][op_idx]
        possible_machines = operation[0]
        possible_times = operation[1]

        # Select machine based on earliest available time
        best_machine = None
        earliest_start_time = float('inf')
        best_processing_time = None

        for i, machine_id in enumerate(possible_machines):
            processing_time = possible_times[i]
            start_time = max(machine_available_time[machine_id], job_completion_time[job_id])

            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine_id
                best_processing_time = processing_time

        start_time = earliest_start_time
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

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
