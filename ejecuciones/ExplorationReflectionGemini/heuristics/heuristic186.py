
def heuristic(input_data):
    """Combines SPT with dynamic load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_operations_scheduled = {job: 0 for job in jobs}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        for job in list(jobs.keys()):
            next_op_index = job_operations_scheduled[job]

            if next_op_index >= len(jobs[job]):
                continue

            machines, times = jobs[job][next_op_index]
            op_num = next_op_index + 1

            best_machine = None
            best_combined_metric = float('inf')
            processing_time = None
            start_time = None

            for i, m in enumerate(machines):
                current_processing_time = times[i]
                available_time = machine_load[m]
                potential_start_time = max(job_completion_times[job], available_time)
                completion_time = potential_start_time + current_processing_time
                load_factor = machine_load[m]

                combined_metric = completion_time + 0.1 * load_factor # Balance Makespan with Load

                if combined_metric < best_combined_metric:
                    best_combined_metric = combined_metric
                    best_machine = m
                    processing_time = current_processing_time
                    start_time = potential_start_time

            if best_machine is not None:
                end_time = start_time + processing_time

                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })

                machine_load[best_machine] = end_time
                job_completion_times[job] = end_time
                job_operations_scheduled[job] += 1

    return schedule
