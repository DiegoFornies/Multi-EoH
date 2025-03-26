
def heuristic(input_data):
    """Combines SPT, load balancing, and dynamic machine selection."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    schedule = {job: [] for job in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_combined_metric = float('inf')

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                completion_time = start_time + processing_time

                load_balance_factor = machine_load[machine]
                # Dynamic weighting based on load
                weight = 0.1 if load_balance_factor < sum(machine_load.values()) / n_machines else 0.05
                combined_metric = completion_time + weight * load_balance_factor

                if combined_metric < min_combined_metric:
                    min_combined_metric = combined_metric
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_time[job] = best_start_time + best_processing_time

    return schedule
