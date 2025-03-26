
def heuristic(input_data):
    """Schedules operations based on earliest due date (EDD)."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    job_due_dates = {}

    # Calculate due dates based on total processing time of each job
    for job_id in range(1, n_jobs + 1):
        total_processing_time = 0
        for operation_data in jobs[job_id]:
            total_processing_time += min(operation_data[1])  # Shortest processing time
        job_due_dates[job_id] = total_processing_time

    # Schedule jobs based on EDD
    job_ids = sorted(jobs.keys(), key=lambda job_id: job_due_dates[job_id])

    for job_id in job_ids:
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            # Choose machine with shortest processing time
            best_machine = possible_machines[0]
            best_processing_time = possible_times[0]
            for i in range(1, len(possible_machines)):
                if possible_times[i] < best_processing_time:
                    best_machine = possible_machines[i]
                    best_processing_time = possible_times[i]

            # Schedule operation on the chosen machine
            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job states
            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
