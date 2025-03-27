
def heuristic(input_data):
    """Schedules operations based on earliest due date (EDD) and shortest processing time (SPT)."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_due_dates = {}
    for job_id in jobs:
        job_due_dates[job_id] = sum(min(times) for machines, times in jobs[job_id])

    job_priority = sorted(job_due_dates.items(), key=lambda item: item[1])

    for job_id, _ in job_priority:
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]

            best_machine = None
            min_end_time = float('inf')

            for m_idx, machine in enumerate(possible_machines):
                processing_time = possible_times[m_idx]
                start_time = max(machine_available_times[machine], current_time)
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_end_time,
                'Processing Time': best_processing_time
            })

            machine_available_times[best_machine] = min_end_time
            current_time = min_end_time

    return schedule
