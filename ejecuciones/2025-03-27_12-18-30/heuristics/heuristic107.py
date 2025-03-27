
def heuristic(input_data):
    """Hybrid heuristic: EDD and SPT for FJSSP with machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Calculate job due dates based on total processing time
    job_due_dates = {}
    for job in range(1, n_jobs + 1):
        total_processing_time = 0
        for machines, times in jobs[job]:
            total_processing_time += min(times)
        job_due_dates[job] = total_processing_time

    # Prioritize jobs based on due date
    job_order = sorted(job_due_dates.items(), key=lambda item: item[1])

    for job, _ in job_order:
        schedule[job] = []
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            best_machine = None
            earliest_start_time = float('inf')
            best_processing_time = None
            min_load = float('inf')

            # Choose machine based on SPT and load balancing
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                
                # SPT with Load Balancing
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
                    min_load = machine_load[machine]
                elif start_time == earliest_start_time and machine_load[machine] < min_load:
                    best_machine = machine
                    best_processing_time = processing_time
                    min_load = machine_load[machine]


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
