
def heuristic(input_data):
    """Schedules jobs minimizing idle time between operations of same job."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    schedule = {}
    job_completion_time = {j: 0 for j in jobs}

    for job in jobs:
        schedule[job] = []
        current_time = 0

        for op_idx, (machines, times) in enumerate(jobs[job]):
            best_machine = None
            min_end_time = float('inf')
            processing_time = None

            for i, machine in enumerate(machines):
                start_time = max(current_time, machine_time[machine])
                end_time = start_time + times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    processing_time = times[i]

            start_time = max(current_time, machine_time[best_machine])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            machine_time[best_machine] = end_time
            current_time = end_time

    return schedule
