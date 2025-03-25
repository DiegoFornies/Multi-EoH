
def heuristic(input_data):
    """Greedy heuristic: Prioritizes machine availability and shorter processing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for op_idx, operation in enumerate(job_operations):
            eligible_machines = operation[0]
            processing_times = operation[1]

            best_machine = -1
            min_end_time = float('inf')
            best_processing_time = -1

            for i, machine in enumerate(eligible_machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_times[i]

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time

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
