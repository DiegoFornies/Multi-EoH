
def heuristic(input_data):
    """Schedules jobs using a Longest Processing Time (LPT) and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    job_total_processing_times = {}
    for job, operations in jobs_data.items():
        job_total_processing_times[job] = sum(max(times) for machines, times in operations)

    job_order = sorted(job_total_processing_times.keys(), key=job_total_processing_times.get, reverse=True)

    for job in job_order:
        schedule[job] = []
        current_time = 0

        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1

            # Choose the machine with the least load
            best_machine, best_processing_time = None, None
            min_load = float('inf')

            for m_idx, machine in enumerate(machines):
                if machine_load[machine] < min_load:
                    min_load = machine_load[machine]
                    best_machine = machine
                    best_processing_time = times[m_idx]

            start_time = max(machine_available_time[best_machine], current_time)
            processing_time = best_processing_time
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += processing_time
            current_time = end_time
            job_completion_time[job] = end_time
    return schedule
