
def heuristic(input_data):
    """Combines earliest availability, machine load, and SPT to schedule jobs."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    schedule = {}

    operation_queue = []
    for job_id in range(1, n_jobs + 1):
        job_operations = jobs[job_id]
        for operation_index, operation_data in enumerate(job_operations):
            min_processing_time = float('inf')
            for time in operation_data[1]:
              min_processing_time = min(min_processing_time, time)
            operation_queue.append((job_id, operation_index, min_processing_time))

    operation_queue.sort(key=lambda x: x[2])

    for job_id, operation_index, _ in operation_queue:
        operation_data = jobs[job_id][operation_index]
        possible_machines = operation_data[0]
        possible_times = operation_data[1]

        best_machine = None
        min_end_time = float('inf')

        for i in range(len(possible_machines)):
            machine = possible_machines[i]
            processing_time = possible_times[i]

            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            end_time = start_time + processing_time
            weighted_end_time = end_time + 0.05 * machine_load[machine]

            if weighted_end_time < min_end_time:
                min_end_time = weighted_end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        machine_available_times[best_machine] = best_start_time + best_processing_time
        machine_load[best_machine] += best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

    return schedule
