
def heuristic(input_data):
    """Earliest Due Date (EDD) with machine selection based on earliest availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    job_due_dates = {}

    # Calculate job due dates (sum of shortest processing times).
    for job_id in range(1, n_jobs + 1):
        due_date = 0
        for machines, times in jobs[job_id]:
            due_date += min(times)
        job_due_dates[job_id] = due_date

    # Sort jobs by due date.
    sorted_jobs = sorted(job_due_dates.items(), key=lambda item: item[1])

    for job_id, _ in sorted_jobs:
        job_operations = jobs[job_id]

        current_start_time = 0
        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            # Select machine with earliest available time.
            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]
                start_time = max(machine_available_time[machine], current_start_time)

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = max(machine_available_time[best_machine], current_start_time)
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            current_start_time = end_time

    return schedule
