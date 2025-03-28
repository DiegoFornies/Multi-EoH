
def heuristic(input_data):
    """Schedules jobs minimizing makespan with SPT and machine load consideration."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []

    for job in jobs_data:
        for op_idx, operation in enumerate(jobs_data[job]):
            machines, times = operation
            op_num = op_idx + 1

            # Shortest Processing Time (SPT)
            min_processing_time = float('inf')
            best_machine = None
            best_start_time = 0

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])

                if processing_time < min_processing_time:
                    min_processing_time = processing_time
                    best_machine = machine
                    best_start_time = start_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + min_processing_time,
                'Processing Time': min_processing_time
            })

            machine_available_time[best_machine] = best_start_time + min_processing_time
            job_completion_time[job] = best_start_time + min_processing_time

    return schedule
