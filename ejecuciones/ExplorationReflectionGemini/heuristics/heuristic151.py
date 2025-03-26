
def heuristic(input_data):
    """FJSSP heuristic: SPT + Load Balance + Job Ready Time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1
            best_machine = None
            min_combined_metric = float('inf')

            for i, machine in enumerate(machines):
                processing_time = times[i]
                available_time = machine_available_time[machine]
                job_ready_time = job_completion_time[job]
                start_time = max(available_time, job_ready_time)
                completion_time = start_time + processing_time
                load_balance_factor = machine_load[machine]

                combined_metric = completion_time + 0.05 * load_balance_factor + 0.01 * job_ready_time

                if combined_metric < min_combined_metric:
                    min_combined_metric = combined_metric
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time

    return schedule
