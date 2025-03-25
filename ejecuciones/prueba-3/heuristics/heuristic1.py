
def heuristic(input_data):
    """
    Heuristic for FJSSP: Chooses the machine with the earliest available time
    for each operation, prioritizing shorter processing times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id, operations in jobs.items():
        schedule[job_id] = []
        for op_idx, operation in enumerate(operations):
            possible_machines = operation[0]
            processing_times = operation[1]

            best_machine = None
            min_end_time = float('inf')

            for i, machine in enumerate(possible_machines):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_times[i]
                    best_start_time = start_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })
            machine_available_times[best_machine] = best_start_time + best_processing_time
            job_completion_times[job_id] = best_start_time + best_processing_time

    return schedule
