
def heuristic(input_data):
    """Heuristic for FJSSP using global makespan minimization."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    operations_list = []
    for job_id in range(1, n_jobs + 1):
        for op_index, operation in enumerate(jobs[job_id]):
            operations_list.append((job_id, op_index, operation))

    operations_list.sort(key=lambda x: min(x[2][1]))

    for job_id, op_index, operation in operations_list:
        eligible_machines = operation[0]
        processing_times = operation[1]

        best_machine = None
        min_makespan = float('inf')
        best_processing_time = None

        for machine_index, machine_id in enumerate(eligible_machines):
            processing_time = processing_times[machine_index]
            start_time = max(machine_available_time[machine_id], job_last_end_time[job_id])
            makespan = start_time + processing_time

            if makespan < min_makespan:
                min_makespan = makespan
                best_machine = machine_id
                best_processing_time = processing_time

        start_time = max(machine_available_time[best_machine], job_last_end_time[job_id])
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_last_end_time[job_id] = end_time

    return schedule
