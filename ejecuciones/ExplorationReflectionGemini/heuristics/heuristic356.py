
def heuristic(input_data):
    """Operation-centric heuristic with earliest finish time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    # Create a list of operations and sort by earliest possible finish time
    operations = []
    for job_id in range(1, n_jobs + 1):
        for operation_index, operation_data in enumerate(jobs[job_id]):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]
            min_finish_time = float('inf')
            best_machine = None
            processing_time = None

            for i, machine in enumerate(possible_machines):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                finish_time = start_time + possible_times[i]
                if finish_time < min_finish_time:
                    min_finish_time = finish_time
                    best_machine = machine
                    processing_time = possible_times[i]

            operations.append({
                'job_id': job_id,
                'operation_index': operation_index,
                'machine': best_machine,
                'processing_time': processing_time,
                'earliest_start_time': max(machine_available_times[best_machine], job_completion_times[job_id]),
                'earliest_finish_time': min_finish_time
            })

    # Sort operations by earliest finish time
    operations.sort(key=lambda x: x['earliest_finish_time'])

    # Schedule operations
    for operation in operations:
        job_id = operation['job_id']
        operation_index = operation['operation_index']
        machine = operation['machine']
        processing_time = operation['processing_time']
        start_time = operation['earliest_start_time']
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_times[machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
