
def heuristic(input_data):
    """Hybrid heuristic: SPT, load balancing, earliest finish time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs[job_id]):
            machines = operation[0]
            processing_times = operation[1]

            best_machine = None
            min_end_time = float('inf')

            for i, machine in enumerate(machines):
                processing_time = processing_times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time
                load_penalty = machine_load[machine] * 0.001

                if end_time + load_penalty < min_end_time:
                    min_end_time = end_time + load_penalty
                    best_machine = machine
                    best_processing_time = processing_time
                    actual_start_time = start_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': actual_start_time,
                'End Time': actual_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = actual_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_time[job_id] = actual_start_time + best_processing_time

    return schedule
