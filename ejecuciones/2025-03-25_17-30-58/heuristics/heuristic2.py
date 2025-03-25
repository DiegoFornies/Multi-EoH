
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem that prioritizes
    operations based on shortest processing time and earliest machine availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    eligible_operations = []
    for job_id, operations in jobs_data.items():
        if operations:
            eligible_operations.append((job_id, 0))  # (job_id, operation_index)

    while eligible_operations:
        # Prioritize operations with shortest processing time and earliest machine availability.
        best_op = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, op_index in eligible_operations:
            machines, times = jobs_data[job_id][op_index]

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_availability[machine], job_completion_times[job_id])
                end_time = start_time + times[m_idx]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_op = (job_id, op_index)
                    best_machine = machine
                    processing_time = times[m_idx]

        # Schedule the best operation
        job_id, op_index = best_op
        start_time = max(machine_availability[best_machine], job_completion_times[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine availability and job completion time
        machine_availability[best_machine] = end_time
        job_completion_times[job_id] = end_time

        # Remove the scheduled operation from eligible operations and add the next operation (if any)
        eligible_operations.remove((job_id, op_index))
        if op_index + 1 < len(jobs_data[job_id]):
            eligible_operations.append((job_id, op_index + 1))

    return schedule
