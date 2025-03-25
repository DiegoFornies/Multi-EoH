
def heuristic(input_data):
    """A combined heuristic for FJSSP, minimizing makespan & idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in jobs}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_end_time = {job: 0 for job in jobs}

    for job, ops in jobs.items():
        for op_idx, op_data in enumerate(ops):
            machines, times = op_data
            best_machine, min_end_time = None, float('inf')

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_end_time[job])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_end_time[job] = best_start_time + best_processing_time

    return schedule
