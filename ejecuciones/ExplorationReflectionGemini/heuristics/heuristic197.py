
def heuristic(input_data):
    """Schedules jobs using Shortest Processing Time and dynamic machine selection."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Sort operations by shortest processing time
    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_index, op_data in enumerate(jobs[job_id]):
            min_time = min(op_data[1])
            operations.append((min_time, job_id, op_index))

    operations.sort()

    for _, job_id, op_index in operations:
        op_data = jobs[job_id][op_index]
        possible_machines = op_data[0]
        possible_times = op_data[1]

        best_machine = None
        min_end_time = float('inf')
        best_processing_time = None

        for i in range(len(possible_machines)):
            machine = possible_machines[i]
            processing_time = possible_times[i]

            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time
                best_start_time = start_time

        if job_id not in schedule:
            schedule[job_id] = []

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
