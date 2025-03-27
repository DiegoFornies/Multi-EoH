
def heuristic(input_data):
    """Schedules operations favoring machines with shorter processing times."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        current_operation = 0

        for operation in jobs[job_id]:
            current_operation += 1
            possible_machines = operation[0]
            possible_times = operation[1]

            # Choose machine that offers shortest time
            best_machine = possible_machines[possible_times.index(min(possible_times))]
            processing_time = min(possible_times)

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': current_operation,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
