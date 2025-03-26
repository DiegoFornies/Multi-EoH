
def heuristic(input_data):
    """FJSSP heuristic: Combines SPT, Earliest Availability, and Load Balancing."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    # Calculate total processing time for each job
    job_total_processing_times = {}
    for job in range(1, n_jobs + 1):
        total_time = 0
        for machines, times in jobs[job]:
            total_time += min(times)
        job_total_processing_times[job] = total_time

    # Prioritize jobs based on shortest processing time
    job_priority = sorted(range(1, n_jobs + 1), key=lambda x: job_total_processing_times[x])

    for job in job_priority:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_combined_metric = float('inf')

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                completion_time = start_time + processing_time

                # Combine earliest availability, and load balance
                load_balance_factor = machine_load[machine]
                combined_metric = completion_time + 0.05 * load_balance_factor + start_time*0.01

                if combined_metric < min_combined_metric:
                    min_combined_metric = combined_metric
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

            machine_available_time[best_machine] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_time[job] = best_start_time + best_processing_time

    return schedule
