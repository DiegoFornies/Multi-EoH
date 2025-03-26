
def heuristic(input_data):
    """Earliest Due Date (EDD) scheduling."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Calculate due date for each job based on total processing time
    job_due_dates = {}
    for job_id in range(1, n_jobs + 1):
        total_processing_time = 0
        for operation_data in jobs[job_id]:
            total_processing_time += min(operation_data[1]) # Shortest time for each operation
        job_due_dates[job_id] = total_processing_time

    # Sort jobs by due date (EDD)
    sorted_jobs = sorted(range(1, n_jobs + 1), key=lambda x: job_due_dates[x])

    for job_id in sorted_jobs:
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            # Find the machine with the earliest available time
            best_machine = None
            min_available_time = float('inf')
            best_processing_time = None

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]
                available_time = machine_available_times[machine]
                if available_time < min_available_time:
                    min_available_time = available_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule operation to the best machine found
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
