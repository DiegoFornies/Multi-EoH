
def heuristic(input_data):
    """Schedules jobs considering machine load, availability, and dynamic delay."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            # Dynamic delay factor based on machine load variance
            load_values = list(machine_load.values())
            if load_values:
                load_variance = sum([(x - sum(load_values) / len(load_values)) ** 2 for x in load_values]) / len(load_values)
                delay_factor = 0.01 * load_variance
            else:
                delay_factor = 0.01

            # Find the best machine
            best_machine = None
            min_combined_score = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time
                load_penalty = machine_load[machine] * delay_factor  # Load aware penalty
                combined_score = machine_load[machine] + end_time + load_penalty

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
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

            machine_load[best_machine] = best_start_time + best_processing_time # Using end time to consider processing time
            machine_available_time[best_machine] = best_start_time + best_processing_time # Using end time to consider processing time
            job_completion_time[job] = best_start_time + best_processing_time # Using end time to consider processing time

    return schedule
