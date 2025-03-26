
def heuristic(input_data):
    """Operation-centric heuristic for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_operations_done = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    eligible_operations = []
    for job_id in range(1, n_jobs + 1):
        eligible_operations.append((job_id, 0))  # (job_id, operation_index)

    while eligible_operations:
        best_operation = None
        best_machine = None
        earliest_start_time = float('inf')

        for job_id, operation_index in eligible_operations:
            operation_data = jobs[job_id][operation_index]
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]

                available_time = machine_available_time[machine]
                start_time = available_time
                
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_operation = (job_id, operation_index)
                    best_machine = machine
                    best_processing_time = processing_time

        job_id, operation_index = best_operation
        machine = best_machine

        start_time = machine_available_time[machine]
        end_time = start_time + best_processing_time

        machine_available_time[machine] = end_time
        
        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        eligible_operations.remove((job_id, operation_index))
        job_operations_done[job_id] += 1

        if job_operations_done[job_id] < len(jobs[job_id]):
            eligible_operations.append((job_id, job_operations_done[job_id]))

    return schedule
