
def heuristic(input_data):
    """Schedules jobs using EFT, load balancing, and dynamic tie-breaking."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_workload = {m: 0 for m in range(n_machines)}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        best_machine = None
        best_processing_time = float('inf')
        earliest_completion_time = float('inf')
        tie_breaker = float('inf')

        total_workload = sum(machine_workload.values())
        load_variance = sum([(workload - (total_workload / n_machines)) ** 2 for workload in machine_workload.values()]) / n_machines if n_machines > 0 else 0
        delay_factor = 0.001 * load_variance  # Reduced delay factor

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            for machine_id, processing_time in zip(machines, times):
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                completion_time = start_time + processing_time
                workload = machine_workload[machine_id]

                load_penalty = workload * delay_factor  # Adjusted load penalty
                weighted_completion = completion_time + load_penalty

                tie_break_value = weighted_completion + (workload / (total_workload + 1e-6)) * 0.1 # workload factor, reduced magnitude

                if weighted_completion < earliest_completion_time or \
                   (weighted_completion == earliest_completion_time and tie_break_value < tie_breaker):
                    earliest_completion_time = weighted_completion
                    best_job, best_op_index = job_id, op_index
                    best_machine, best_processing_time = machine_id, processing_time
                    tie_breaker = tie_break_value

        if best_job is None:
            print("Error: No suitable operation found.")
            return schedule

        job_id, op_index = best_job, best_op_index

        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_workload[best_machine] += best_processing_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        ready_operations.remove((job_id, op_index))

        if op_index + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_index + 1))

    return schedule
