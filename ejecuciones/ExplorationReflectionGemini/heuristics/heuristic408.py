
def heuristic(input_data):
    """FJSSP heuristic: SPT, load balancing, and urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_weighted_time = float('inf')

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]

                start_time = max(machine_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                weighted_time = 0.7 * end_time + 0.3 * machine_time[machine]  # SPT + Load balancing

                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            machine_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job_id] = best_start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })
    return schedule
