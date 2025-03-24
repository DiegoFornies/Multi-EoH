
def heuristic(input_data):
    """
    Schedules operations by prioritizing shortest processing time and earliest machine availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of operations to schedule
    operations = []
    for job_id, job_ops in jobs_data.items():
        for op_id, op_data in enumerate(job_ops):
            operations.append((job_id, op_id + 1, op_data))  # (job_id, operation_number, operation_data)

    # Sort operations based on shortest processing time
    operations.sort(key=lambda op: min(op[2][1]))

    for job_id, op_num, op_data in operations:
        machines, times = op_data

        best_machine = None
        min_end_time = float('inf')

        # Find the best machine for the operation
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + times[i]

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = times[i]
                start = start_time

        # Schedule the operation on the best machine
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start,
            'End Time': min_end_time,
            'Processing Time': processing_time
        })

        # Update machine availability and job completion time
        machine_available_time[best_machine] = min_end_time
        job_completion_time[job_id] = min_end_time

    return schedule
