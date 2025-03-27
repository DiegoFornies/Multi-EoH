
def heuristic(input_data):
    """Schedules jobs, prioritizing shortest processing time to minimize makespan."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        for op_idx, op_data in enumerate(jobs[job_id]):
            machines, times = op_data
            op_num = op_idx + 1

            best_machine = None
            min_processing_time = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                if processing_time < min_processing_time:
                    min_processing_time = processing_time
                    best_machine = machine

            if best_machine is not None:
                start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
                end_time = start_time + min_processing_time
                schedule[job_id].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': min_processing_time
                })

                machine_available_time[best_machine] = end_time
                job_completion_time[job_id] = end_time

    return schedule
