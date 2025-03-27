
def heuristic(input_data):
    """Prioritizes operations with shortest processing time first."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of all operations with their attributes
    all_operations = []
    for job_id in range(1, n_jobs + 1):
        for op_index, operation in enumerate(jobs[job_id]):
            eligible_machines = operation[0]
            processing_times = operation[1]

            # Store the minimum processing time for this operation
            min_processing_time = min(processing_times)
            all_operations.append({
                'job_id': job_id,
                'op_index': op_index,
                'eligible_machines': eligible_machines,
                'processing_times': processing_times,
                'min_processing_time': min_processing_time
            })

    # Sort operations based on the shortest processing time
    all_operations = sorted(all_operations, key=lambda x: x['min_processing_time'])

    # Schedule each operation
    for operation in all_operations:
        job_id = operation['job_id']
        op_index = operation['op_index']
        eligible_machines = operation['eligible_machines']
        processing_times = operation['processing_times']

        best_machine = None
        min_completion_time = float('inf')
        best_processing_time = None
        machine_index_selected = None
        for machine_index, machine_id in enumerate(eligible_machines):
            completion_time = max(machine_available_time[machine_id],
                                  job_completion_time[job_id]) + processing_times[machine_index]

            if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = machine_id
                best_processing_time = processing_times[machine_index]
                machine_index_selected = machine_index

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_processing_time
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
