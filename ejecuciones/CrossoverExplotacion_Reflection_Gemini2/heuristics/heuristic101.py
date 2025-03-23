
def heuristic(input_data):
    """
    A hybrid heuristic for FJSSP combining earliest finish time,
    SPT, and machine load balancing with a dynamic delay factor.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, processing_times = operation
            best_machine = None
            min_end_time = float('inf')
            min_processing_time = float('inf')

            # Dynamic delay factor based on machine load variance
            load_values = list(machine_load.values())
            if load_values:
                load_variance = sum([(x - sum(load_values) / len(load_values)) ** 2 for x in load_values]) / len(load_values)
                delay_factor = 0.01 * load_variance
            else:
                delay_factor = 0.01
            for i, machine in enumerate(machines):
                processing_time = processing_times[i]
                start_time = max(machine_available[machine], job_completion[job_id])
                end_time = start_time + processing_time
                load_penalty = machine_load[machine] * delay_factor

                combined_score = end_time + load_penalty

                if combined_score < min_end_time:
                    min_end_time = combined_score
                    best_machine = machine
                    best_processing_time = processing_time

                elif combined_score == min_end_time and processing_time < min_processing_time:
                    min_processing_time = processing_time
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = max(machine_available[best_machine], job_completion[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available[best_machine] = end_time
            job_completion[job_id] = end_time
            machine_load[best_machine] += best_processing_time

    return schedule
