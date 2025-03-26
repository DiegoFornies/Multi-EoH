
def heuristic(input_data):
    """Prioritizes operations based on remaining processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    remaining_times = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        remaining_times[job_id] = sum(sum(times) / len(times) for machines, times in jobs[job_id])

    all_operations = []
    for job_id in range(1, n_jobs + 1):
        for operation_index, operation_data in enumerate(jobs[job_id]):
            all_operations.append((remaining_times[job_id], job_id, operation_index, operation_data))

    all_operations.sort(key=lambda x: x[0], reverse=True) #sort all operations.

    for remaining_time, job_id, operation_index, operation_data in all_operations:
        possible_machines = operation_data[0]
        possible_times = operation_data[1]

        best_machine = None
        best_processing_time = None
        earliest_start_time = float('inf')

        for i in range(len(possible_machines)):
            machine = possible_machines[i]
            processing_time = possible_times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job_id])

            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        start_time = earliest_start_time
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        remaining_times[job_id] -= best_processing_time


    return schedule
