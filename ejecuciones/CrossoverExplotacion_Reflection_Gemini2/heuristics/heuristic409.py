
def heuristic(input_data):
    """Combines EFT, machine load balancing, and job dependencies."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        best_machine, best_processing_time = None, float('inf')
        earliest_finish = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            for machine_id, processing_time in zip(machines, times):
                start_time = max(machine_available_times[machine_id], job_completion_times[job_id])
                finish_time = start_time + processing_time

                # Dynamic delay factor based on machine load variance
                load_values = list(machine_load.values())
                if load_values:
                    load_variance = sum([(x - sum(load_values) / len(load_values)) ** 2 for x in load_values]) / len(load_values)
                    delay_factor = 0.01 * load_variance
                else:
                    delay_factor = 0.01

                weighted_finish = 0.7 * finish_time + 0.3 * machine_load[machine_id] + delay_factor + machine_id * 0.0001

                if weighted_finish < earliest_finish:
                    earliest_finish = weighted_finish
                    best_job, best_op_index = job_id, op_index
                    best_machine, best_processing_time = machine_id, processing_time

        job_id, op_index = best_job, best_op_index
        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_load[best_machine] += best_processing_time

        ready_operations.remove((job_id, op_index))
        if op_index + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_index + 1))

    return schedule
