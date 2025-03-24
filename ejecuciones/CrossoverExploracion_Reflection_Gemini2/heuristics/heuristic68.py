
def heuristic(input_data):
    """Combines SPT, machine load, and job completion time for scheduling."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}

    for job_id in jobs_data:
        for op_idx, operation in enumerate(jobs_data[job_id]):
            machines, processing_times = operation
            op_num = op_idx + 1

            best_machine = None
            min_end_time = float('inf')
            processing_time = None

            for i, machine in enumerate(machines):
                time = processing_times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    processing_time = time

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
