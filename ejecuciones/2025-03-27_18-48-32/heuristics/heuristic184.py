
def heuristic(input_data):
    """Combines SPT, EDD, and adaptive load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}  # Track completion time of each job
    job_due_dates = {j: 0 for j in range(1, n_jobs + 1)}

    # Initialize job due dates (simplified: sum of processing times)
    for job_id in range(1, n_jobs + 1):
        total_processing_time = 0
        for operation in jobs[job_id]:
            total_processing_time += min(operation[1])
        job_due_dates[job_id] = total_processing_time  # Placeholder

    eligible_operations = []
    for job in range(1, n_jobs + 1):
        eligible_operations.append((job, 1))

    while eligible_operations:
        best_op = None
        min_score = float('inf')
        best_machine = None
        best_time = None
        best_job = None

        for job, op_idx in eligible_operations:
            operation = jobs[job][op_idx - 1]
            possible_machines = operation[0]
            possible_times = operation[1]

            for machine_idx, machine in enumerate(possible_machines):
                processing_time = possible_times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_times[job])
                end_time = start_time + processing_time

                # Adaptive load balancing
                load_factor = 1 + (machine_load[machine] / (sum(machine_load.values()) + 1e-9))  # Avoid division by zero
                adjusted_end_time = end_time * load_factor

                # EDD component
                job_urgency = job_due_dates[job] - start_time

                # SPT component
                spt = processing_time

                # Combine criteria
                score = adjusted_end_time + (0.1 * max(0, -job_urgency)) + spt # Adjust weights

                if score < min_score:
                    min_score = score
                    best_machine = machine
                    best_time = processing_time
                    best_op = op_idx
                    best_job = job

        start_time = max(machine_available_time[best_machine], job_completion_times[best_job])
        end_time = start_time + best_time

        if best_job not in schedule:
            schedule[best_job] = []

        schedule[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_time[best_machine] = end_time
        machine_load[best_machine] += best_time
        job_completion_times[best_job] = end_time

        eligible_operations.remove((best_job, best_op))

        if best_op < len(jobs[best_job]):
            eligible_operations.append((best_job, best_op + 1))

    return schedule
