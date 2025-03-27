
def heuristic(input_data):
    """Hybrid heuristic: Shortest Processing Time & Least Loaded Machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}

    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 1))

    while eligible_operations:
        best_op = None
        shortest_processing_time = float('inf')
        least_loaded_machine = None
        best_start_time = float('inf')
        best_job = None
        best_processing_time = None

        for job, op_num in eligible_operations:
            machines, times = jobs_data[job][op_num - 1]

            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_times[job])
                processing_time = times[m_idx]

                if processing_time < shortest_processing_time:
                    shortest_processing_time = processing_time
                    least_loaded_machine = m
                    best_start_time = start_time
                    best_op = op_num
                    best_job = job
                    best_processing_time = processing_time
                elif processing_time == shortest_processing_time:
                    if machine_available_times[m] < machine_available_times[least_loaded_machine]:
                        least_loaded_machine = m
                        best_start_time = start_time
                        best_op = op_num
                        best_job = job
                        best_processing_time = processing_time

        start_time = max(machine_available_times[least_loaded_machine], job_completion_times[best_job])
        end_time = start_time + best_processing_time

        scheduled_operations[best_job].append({
            'Operation': best_op,
            'Assigned Machine': least_loaded_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[least_loaded_machine] = end_time
        job_completion_times[best_job] = end_time

        eligible_operations.remove((best_job, best_op))

        if best_op < len(jobs_data[best_job]):
            eligible_operations.append((best_job, best_op + 1))

    return scheduled_operations
