
def heuristic(input_data):
    """Minimizes makespan via shortest processing time (SPT) and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        operations = jobs[job_id]

        for op_idx, operation_data in enumerate(operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]
            op_num = op_idx + 1

            best_machine = None
            min_completion_time = float('inf')

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                completion_time = start_time + processing_time

                # SPT first then load balancing.
                weighted_completion_time = completion_time + 0.1 * machine_load[machine]

                if weighted_completion_time < min_completion_time:
                    min_completion_time = weighted_completion_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            machine_available_time[best_machine] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_time[job_id] = best_start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

    return schedule
