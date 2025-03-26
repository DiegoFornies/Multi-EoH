
def heuristic(input_data):
    """Operation-centric scheduling with lookahead for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    remaining_operations = {}  # Track operations to schedule

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        remaining_operations[job_id] = 0

    unscheduled_operations = []
    for job_id in range(1, n_jobs + 1):
        unscheduled_operations.append((job_id, 0))

    while unscheduled_operations:
        best_operation = None
        best_machine = None
        min_makespan_increase = float('inf')

        for job_id, operation_index in unscheduled_operations:
            operation_data = jobs[job_id][operation_index]
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            for i, machine in enumerate(possible_machines):
                processing_time = possible_times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                # Estimate makespan increase
                makespan_increase = end_time - machine_available_times[machine] if end_time > machine_available_times[machine] else 0

                if makespan_increase < min_makespan_increase:
                    min_makespan_increase = makespan_increase
                    best_operation = (job_id, operation_index)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        job_id, operation_index = best_operation
        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time

        unscheduled_operations.remove((job_id, operation_index))
        if operation_index + 1 < len(jobs[job_id]):
            unscheduled_operations.append((job_id, operation_index + 1))

    return schedule
