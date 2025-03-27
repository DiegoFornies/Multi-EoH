
def heuristic(input_data):
    """Schedules jobs balancing SPT and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 1))

    while eligible_operations:
        best_op = None
        best_machine = None
        best_time = float('inf')
        best_job = None

        for job, op_num in eligible_operations:
            machines, times = jobs_data[job][op_num - 1]

            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_times[job])
                processing_time = times[m_idx]

                # Prioritize shorter processing times and balance machine load.
                # SPT primarily, adjusted by current machine load.
                score = processing_time + machine_load[m] * 0.05  # Adjust factor
                
                if score < best_time:
                    best_time = score
                    best_op = op_num
                    best_machine = m
                    best_job = job

        start_time = max(machine_available_times[best_machine], job_completion_times[best_job])
        end_time = start_time + jobs_data[best_job][best_op - 1][1][jobs_data[best_job][best_op - 1][0].index(best_machine)]
        processing_time = jobs_data[best_job][best_op - 1][1][jobs_data[best_job][best_op - 1][0].index(best_machine)]

        scheduled_operations[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[best_job] = end_time
        machine_load[best_machine] += processing_time

        eligible_operations.remove((best_job, best_op))

        if best_op < len(jobs_data[best_job]):
            eligible_operations.append((best_job, best_op + 1))

    return scheduled_operations
