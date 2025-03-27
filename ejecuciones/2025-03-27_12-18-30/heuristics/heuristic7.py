
def heuristic(input_data):
    """
    Heuristic for FJSSP scheduling, considering earliest start time and shortest processing time.
    Schedules operations based on minimizing both machine idle time and operation duration.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in jobs}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}

    # Flatten the operations list to make it easier to iterate over
    operations_list = []
    for job_id, job_ops in jobs.items():
        for op_index, op_details in enumerate(job_ops):
            operations_list.append((job_id, op_index, op_details))

    # Sort operations by shortest processing time first (SPT) and earliest job time
    operations_list.sort(key=lambda x: (min(x[2][1]), job_completion_time[x[0]]))
    
    for job_id, op_index, op_details in operations_list:
        available_machines = op_details[0]
        processing_times = op_details[1]

        best_machine = None
        min_end_time = float('inf')

        for i, machine in enumerate(available_machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_times[i]

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_times[i]
                best_start_time = start_time


        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job_id] = best_start_time + best_processing_time

    return schedule
