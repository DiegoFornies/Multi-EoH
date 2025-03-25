
def heuristic(input_data):
    """
    Schedules jobs using a machine load balancing heuristic.
    Chooses the machine with the earliest available time for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(1, n_machines + 1)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        operations = jobs[job_id]
        for op_index, operation in enumerate(operations):
            machines, times = operation
            op_number = op_index + 1

            best_machine = None
            min_start_time = float('inf')

            for machine_index, machine in enumerate(machines):
                processing_time = times[machine_index]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
            
            start_time = min_start_time
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_number,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
    return schedule
