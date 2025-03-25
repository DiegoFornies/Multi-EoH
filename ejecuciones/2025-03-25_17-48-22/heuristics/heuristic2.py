
def heuristic(input_data):
    """
    Heuristic for FJSSP: Assigns each operation to the machine with the earliest available time,
    considering both machine and job completion times.
    Prioritizes shorter processing times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data}
    schedule = {job: [] for job in jobs_data}

    for job_id in jobs_data:
        for operation_index, operation in enumerate(jobs_data[job_id]):
            available_machines = operation[0]
            processing_times = operation[1]

            best_machine = None
            min_finish_time = float('inf')
            min_processing_time = float('inf')

            for i, machine_id in enumerate(available_machines):
                processing_time = processing_times[i]
                start_time = max(machine_available_time[machine_id], job_completion_time[job_id])
                finish_time = start_time + processing_time

                if finish_time < min_finish_time or (finish_time == min_finish_time and processing_time < min_processing_time):
                    min_finish_time = finish_time
                    best_machine = machine_id
                    min_processing_time = processing_time
                    best_start_time = start_time

            machine_available_time[best_machine] = min_finish_time
            job_completion_time[job_id] = min_finish_time
            op_num = operation_index + 1
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_finish_time,
                'Processing Time': min_processing_time
            })

    return schedule
