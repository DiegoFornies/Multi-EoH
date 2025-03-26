
def heuristic(input_data):
    """Combines SPT, load balancing, and job urgency dynamically."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    job_remaining_times = {}

    for job_id in range(1, n_jobs + 1):
        remaining_time = 0
        for machines, times in jobs[job_id]:
            remaining_time += min(times)
        job_remaining_times[job_id] = remaining_time

    for job_id in range(1, n_jobs + 1):
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_combined_metric = float('inf')

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]

                start_time = max(machine_available_time[machine], job_completion_times[job_id])
                completion_time = start_time + processing_time

                load_balance_factor = machine_load[machine]
                urgency_factor = job_remaining_times[job_id]

                # Dynamically adjust weights based on machine load and job urgency
                load_weight = 0.1 * (1 + machine_load[machine] / sum(machine_load.values()) if sum(machine_load.values()) > 0 else 1)
                urgency_weight = 0.1 * (1 + job_remaining_times[job_id] / sum(job_remaining_times.values()) if sum(job_remaining_times.values()) > 0 else 1)


                combined_metric = completion_time + load_weight * load_balance_factor - urgency_weight * urgency_factor

                if combined_metric < min_combined_metric:
                    min_combined_metric = combined_metric
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            machine_available_time[best_machine] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_times[job_id] = best_start_time + best_processing_time
            job_remaining_times[job_id] -= best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })
    return schedule
