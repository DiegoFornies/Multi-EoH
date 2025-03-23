
def heuristic(input_data):
    """Combines EFT, load balancing, and dynamic tie-breaking for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        best_machine, best_processing_time = None, float('inf')
        earliest_completion_time = float('inf')
        tie_breaker = float('inf')

        load_values = list(machine_load.values())
        if load_values:
            load_variance = sum([(x - sum(load_values) / len(load_values)) ** 2 for x in load_values]) / len(load_values)
            delay_factor = 0.01 * load_variance
        else:
            delay_factor = 0.01

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            for machine_id, processing_time in zip(machines, times):
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                completion_time = start_time + processing_time

                # Combined metric: Completion time + Workload factor + Delay
                workload_factor = (machine_load[machine_id] / (sum(machine_load.values()) + 1e-6)) * 5
                load_penalty = machine_load[machine_id] * delay_factor
                combined_metric = completion_time + workload_factor + load_penalty # Completion Time + Workload + Delay

                # Tie-breaking: Prioritize remaining operations and slightly less loaded machines
                remaining_ops = len(jobs_data[job_id]) - (op_index + 1)
                tie_break_value = combined_metric + remaining_ops * 0.01 + machine_load[machine_id] * 0.001 # tie breaker

                if combined_metric < earliest_completion_time or (combined_metric == earliest_completion_time and tie_break_value < tie_breaker):
                    earliest_completion_time = combined_metric
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
        machine_load[best_machine] += best_processing_time

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
