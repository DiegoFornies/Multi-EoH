
def heuristic(input_data):
    """FJSSP heuristic combining load balancing & job precedence."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    job_total_processing_times = {}
    for job in range(1, n_jobs + 1):
        total_time = 0
        for machines, times in jobs[job]:
            total_time += min(times)
        job_total_processing_times[job] = total_time

    available_jobs = sorted(range(1, n_jobs + 1), key=lambda x: job_total_processing_times[x])

    job_operations_scheduled = {job: 0 for job in range(1, n_jobs + 1)}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in range(1, n_jobs + 1)):
        for job in range(1, n_jobs + 1):
            next_op_index = job_operations_scheduled[job]

            if next_op_index >= len(jobs[job]):
                continue

            machines, times = jobs[job][next_op_index]
            op_num = next_op_index + 1

            best_machine = None
            min_completion_time = float('inf')
            best_processing_time = None

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_load[machine], job_completion_times[job])
                completion_time = start_time + processing_time

                load_balance_factor = machine_load[machine]

                combined_metric = completion_time + 0.1 * load_balance_factor  # Adjust the factor 0.1

                if combined_metric < min_completion_time:
                    min_completion_time = combined_metric
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time
                    

            if best_machine is not None:
                start_time = max(machine_load[best_machine], job_completion_times[job])
                end_time = start_time + best_processing_time

                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': best_processing_time
                })

                machine_load[best_machine] = end_time
                job_completion_times[job] = end_time
                job_operations_scheduled[job] += 1

    return schedule
