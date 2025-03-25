
def heuristic(input_data):
    """
    Schedules jobs heuristically, minimizing makespan and balancing machine load.
    Assigns operations to machines based on earliest available time and shortest processing time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job = jobs[job_id]
        for operation_index, operation in enumerate(job):
            machines, times = operation
            best_machine = None
            min_end_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_end_time,
                'Processing Time': best_processing_time
            })

            machine_available_times[best_machine] = min_end_time
            job_completion_times[job_id] = min_end_time

    return schedule
