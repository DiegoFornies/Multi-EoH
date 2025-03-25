
def heuristic(input_data):
    """
    Heuristic to schedule jobs considering earliest start time
    on available machines and minimizing idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs_data:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs_data[job]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine, best_time, earliest_start = None, float('inf'), float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                available_time = machine_available_time[machine]
                start_time = max(available_time, job_completion_time[job])

                if start_time < earliest_start:
                    earliest_start = start_time
                    best_machine = machine
                    best_time = processing_time
                    
            start_time = earliest_start
            end_time = start_time + best_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
