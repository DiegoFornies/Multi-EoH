
def heuristic(input_data):
    """Minimize makespan, balance load dynamically."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            best_machine = None
            earliest_start_time = float('inf')
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])

                # Dynamically adjust the importance of start time and load.
                load_penalty = machine_load[machine]
                combined_score = start_time + 0.1 * load_penalty  # Adjust 0.1 dynamically.

                if combined_score < earliest_start_time:
                    earliest_start_time = combined_score
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = max(machine_available_time[best_machine], job_completion_time[job])
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += best_processing_time
            job_completion_time[job] = end_time

    return schedule
