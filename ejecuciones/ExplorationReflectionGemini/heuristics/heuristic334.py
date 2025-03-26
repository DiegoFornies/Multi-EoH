
def heuristic(input_data):
    """Schedules jobs, minimizing makespan and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of operations with job and operation indices.
    operations = []
    for job_id in range(1, n_jobs + 1):
        for operation_index, operation_data in enumerate(jobs[job_id]):
            operations.append((job_id, operation_index))

    # Sort operations based on shortest processing time (SPT) of the first available machine.
    operations.sort(key=lambda x: min(input_data['jobs'][x[0]][x[1]][1]))

    for job_id, operation_index in operations:
        operation_data = jobs[job_id][operation_index]
        possible_machines = operation_data[0]
        possible_times = operation_data[1]

        best_machine = None
        min_completion_time = float('inf')

        for i in range(len(possible_machines)):
            machine = possible_machines[i]
            processing_time = possible_times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            completion_time = start_time + processing_time

            if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job_id] = best_start_time + best_processing_time

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

    return schedule
