
def heuristic(input_data):
    """Schedules jobs based on earliest finish time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    eligible_operations = []
    for job_id in jobs:
        eligible_operations.append((job_id, 0))

    while eligible_operations:
        best_finish_time = float('inf')
        best_operation = None
        best_machine = None
        best_processing_time = None

        for job_id, op_idx in eligible_operations:
            machines, times = jobs[job_id][op_idx]
            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                finish_time = start_time + processing_time

                if finish_time < best_finish_time:
                    best_finish_time = finish_time
                    best_operation = (job_id, op_idx)
                    best_machine = machine
                    best_processing_time = processing_time

        job_id, op_idx = best_operation
        op_num = op_idx + 1

        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

        eligible_operations.remove(best_operation)

        if op_idx + 1 < len(jobs[job_id]):
            eligible_operations.append((job_id, op_idx + 1))

    return schedule
