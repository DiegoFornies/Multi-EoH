
def heuristic(input_data):
    """FJSSP heuristic using priority scheduling."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_operations_done = {j: 0 for j in range(1, n_jobs + 1)}

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        operations = jobs[job_id]
        if len(operations) > 0:
          available_operations.append((job_id, 0))

    while available_operations:
        # Find operation with shortest processing time available
        best_operation = None
        min_end_time = float('inf')

        for job_id, op_index in available_operations:
            operation = jobs[job_id][op_index]
            eligible_machines = operation[0]
            processing_times = operation[1]

            for machine_index, machine_id in enumerate(eligible_machines):
                processing_time = processing_times[machine_index]
                available_time = machine_available_time[machine_id]

                end_time = available_time + processing_time
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_operation = (job_id, op_index, machine_id, processing_time)

        job_id, op_index, assigned_machine, processing_time = best_operation
        available_operations.remove((job_id, op_index))

        start_time = machine_available_time[assigned_machine]
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[assigned_machine] = end_time
        job_operations_done[job_id] += 1

        if job_operations_done[job_id] < len(jobs[job_id]):
            available_operations.append((job_id, job_operations_done[job_id]))

    return schedule
