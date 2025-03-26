
def heuristic(input_data):
    """Schedules jobs using a global earliest finish time strategy."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    operations = []

    for job_id in range(1, n_jobs + 1):
        for operation_index in range(len(jobs[job_id])):
            operations.append((job_id, operation_index))

    while operations:
        best_job = None
        best_operation = None
        best_machine = None
        min_finish_time = float('inf')

        for job_id, operation_index in operations:
            operation_data = jobs[job_id][operation_index]
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                finish_time = start_time + processing_time

                if finish_time < min_finish_time:
                    min_finish_time = finish_time
                    best_job = job_id
                    best_operation = operation_index
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        operations.remove((best_job, best_operation))

        machine_available_times[best_machine] = best_start_time + best_processing_time
        job_completion_times[best_job] = best_start_time + best_processing_time

        if best_job not in schedule:
            schedule[best_job] = []
        schedule[best_job].append({
            'Operation': best_operation + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

    return schedule
