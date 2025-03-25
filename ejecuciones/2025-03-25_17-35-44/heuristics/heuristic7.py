
def heuristic(input_data):
    """Schedules jobs using a shortest processing time (SPT) and earliest start time (EST) rule."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Flatten operations and sort them by shortest processing time
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, machines, times))

    # Prioritize operations based on shortest processing time first
    operations.sort(key=lambda x: min(x[3]))

    for job_id, op_num, machines, times in operations:
        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            available_time = machine_available_time[machine]
            start_time = max(available_time, job_completion_time[job_id])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        end_time = best_start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
