
def heuristic(input_data):
    """Hybrid heuristic: SPT for jobs, balanced machine selection."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    uncompleted_jobs = set(jobs.keys())

    while uncompleted_jobs:
        # Prioritize job with shortest remaining processing time (SPT)
        current_job = None
        min_remaining_time = float('inf')
        for job_id in uncompleted_jobs:
            remaining_time = 0
            job_operations = jobs[job_id]
            scheduled_operations = len(schedule[job_id])
            for i in range(scheduled_operations, len(job_operations)):
                remaining_time += min(job_operations[i][1])

            if remaining_time < min_remaining_time:
                min_remaining_time = remaining_time
                current_job = job_id

        job_operations = jobs[current_job]
        operation_index = len(schedule[current_job])
        operation_data = job_operations[operation_index]
        possible_machines = operation_data[0]
        possible_times = operation_data[1]

        # Schedule on machine minimizing completion time + load.
        best_machine = None
        min_weighted_time = float('inf')

        for i in range(len(possible_machines)):
            machine = possible_machines[i]
            processing_time = possible_times[i]
            start_time = max(machine_available_times[machine], job_completion_times[current_job])
            end_time = start_time + processing_time
            weighted_time = end_time + 0.2 * machine_load[machine]

            if weighted_time < min_weighted_time:
                min_weighted_time = weighted_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        schedule[current_job].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = best_start_time + best_processing_time
        machine_load[best_machine] += best_processing_time
        job_completion_times[current_job] = best_start_time + best_processing_time

        if len(schedule[current_job]) == len(job_operations):
            uncompleted_jobs.remove(current_job)

    return schedule
