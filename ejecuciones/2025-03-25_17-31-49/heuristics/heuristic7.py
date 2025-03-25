
def heuristic(input_data):
    """Schedules jobs using a shortest processing time and earliest start time heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}

    for job_id in jobs:
        schedule[job_id] = []

    # Flatten the jobs into a list of operations with job_id and operation_index
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((job_id, op_idx, op_data))

    # Sort operations by shortest processing time first, then job_id.
    operations.sort(key=lambda x: min(x[2][1]))  # Prioritize by shortest processing time

    for job_id, op_idx, op_data in operations:
        machines, times = op_data

        best_machine = None
        earliest_start_time = float('inf')
        best_processing_time = None
        
        for i, machine in enumerate(machines):
            processing_time = times[i]
            available_time = machine_available_times[machine]
            start_time = max(available_time, job_completion_times[job_id])

            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        start_time = earliest_start_time
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        
    return schedule
