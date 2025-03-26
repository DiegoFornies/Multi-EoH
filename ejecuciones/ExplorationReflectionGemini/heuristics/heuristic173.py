
def heuristic(input_data):
    """Schedules jobs based on earliest finish time and load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Create a list of all operations
    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_index in range(len(jobs[job_id])):
            operations.append((job_id, op_index))

    # Schedule operations based on earliest finish time
    while operations:
        best_op = None
        earliest_finish_time = float('inf')

        for job_id, op_index in operations:
            operation_data = jobs[job_id][op_index]
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                finish_time = start_time + processing_time

                if finish_time < earliest_finish_time:
                    earliest_finish_time = finish_time
                    best_op = (job_id, op_index, machine, start_time, processing_time)

        # Schedule the best operation
        job_id, op_index, machine, start_time, processing_time = best_op
        machine_available_times[machine] = start_time + processing_time
        job_completion_times[job_id] = start_time + processing_time
        operations.remove((job_id, op_index))

        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': start_time + processing_time,
            'Processing Time': processing_time
        })

    return schedule
