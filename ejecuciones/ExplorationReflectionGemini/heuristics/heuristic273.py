
def heuristic(input_data):
    """Dynamic prioritization based on remaining work and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    remaining_work = {j: sum(min(t) for _, t in ops) for j, ops in jobs.items()}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    scheduled_operations = {job_id: 0 for job_id in range(1, n_jobs + 1)}

    while any(scheduled_operations[j] < len(jobs[j]) for j in range(1, n_jobs + 1)):
        eligible_operations = []
        for job_id in range(1, n_jobs + 1):
            if scheduled_operations[job_id] < len(jobs[job_id]):
                eligible_operations.append(job_id)

        # Prioritize jobs with less remaining work to avoid long delays.
        eligible_operations = sorted(eligible_operations, key=lambda j: remaining_work[j])

        for job_id in eligible_operations:
            operation_index = scheduled_operations[job_id]
            operation_data = jobs[job_id][operation_index]
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_finish_time = float('inf')
            best_processing_time = None

            for i, machine in enumerate(possible_machines):
                processing_time = possible_times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                finish_time = start_time + processing_time

                if finish_time < min_finish_time:
                    min_finish_time = finish_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_times[best_machine] = best_start_time + best_processing_time
            job_completion_times[job_id] = best_start_time + best_processing_time
            remaining_work[job_id] -= best_processing_time
            scheduled_operations[job_id] += 1

    return schedule
