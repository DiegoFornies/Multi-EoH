
def heuristic(input_data):
    """Prioritizes operations with shortest processing time on least loaded machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_finish_times = {job: 0 for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    schedule = {}

    for job in range(1, n_jobs + 1):
        schedule[job] = []

    operations = []
    for job in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs_data[job]):
            operations.append((job, op_idx + 1, operation))

    while operations:
        best_op = None
        best_machine = None
        min_finish_time = float('inf')

        for job, op_num, operation in operations:
            available_machines, processing_times = operation
            for i, machine in enumerate(available_machines):
                processing_time = processing_times[i]
                start_time = max(machine_available_time[machine], job_finish_times[job])
                finish_time = start_time + processing_time

                if finish_time < min_finish_time:
                    min_finish_time = finish_time
                    best_op = (job, op_num, operation)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        job, op_num, operation = best_op
        available_machines, processing_times = operation
        machine = best_machine

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_load[machine] += best_processing_time
        machine_available_time[machine] = best_start_time + best_processing_time
        job_finish_times[job] = best_start_time + best_processing_time
        operations.remove(best_op)

    return schedule
