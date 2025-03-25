
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) that assigns
    operations to machines based on minimizing the earliest completion time,
    taking into account machine availability and job sequencing constraints.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data}
    schedule = {job: [] for job in jobs_data}

    for job_id in jobs_data:
        for operation_index, operation_data in enumerate(jobs_data[job_id]):
            machines, times = operation_data
            best_machine = None
            min_completion_time = float('inf')
            best_processing_time = None

            for machine_index, machine_id in enumerate(machines):
                processing_time = times[machine_index]
                start_time = max(machine_available_time[machine_id], job_completion_time[job_id])
                completion_time = start_time + processing_time

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine_id
                    best_processing_time = processing_time

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time
            operation_number = operation_index + 1

            schedule[job_id].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
