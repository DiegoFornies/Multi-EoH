
def heuristic(input_data):
    """Operation-centric heuristic with lookahead."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    #Sort operations based on processing time across available machines
    operations = []
    for job_id in range(1, n_jobs + 1):
        for operation_index, operation_data in enumerate(jobs[job_id]):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]
            min_time = min(possible_times)
            operations.append((min_time, job_id, operation_index))

    operations.sort()  # SPT based on operation minimum processing time
    
    for _, job_id, operation_index in operations:

        if job_id not in schedule:
            schedule[job_id] = []
            
        operation_data = jobs[job_id][operation_index]
        possible_machines = operation_data[0]
        possible_times = operation_data[1]

        best_machine = None
        min_end_time = float('inf')

        for i, machine in enumerate(possible_machines):
            processing_time = possible_times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time

    return schedule
