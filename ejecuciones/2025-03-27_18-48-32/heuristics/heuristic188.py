
def heuristic(input_data):
    """Combines EDD and SPT, weighting dynamically by operation urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_due_dates = {j: sum(sum(op[1]) / len(op[1]) for op in jobs[j]) * 2 for j in range(1, n_jobs + 1)} # Estimated Due Dates

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]

            best_machine = None
            min_weighted_time = float('inf')

            for machine in possible_machines:
                processing_time = possible_times[possible_machines.index(machine)]
                start_time = max(machine_available_time[machine], current_time)
                end_time = start_time + processing_time

                # Urgency factor: (Due Date - Current Time) / Processing Time
                urgency = (job_due_dates[job_id] - current_time) / processing_time if processing_time > 0 else float('inf')
                # Combine SPT (processing_time) and EDD (urgency)
                weighted_time = processing_time / (urgency + 1) # SPT / Urgency

                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_machine = machine

            processing_time = possible_times[possible_machines.index(best_machine)]
            start_time = max(machine_available_time[best_machine], current_time)
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            current_time = end_time

    return schedule
