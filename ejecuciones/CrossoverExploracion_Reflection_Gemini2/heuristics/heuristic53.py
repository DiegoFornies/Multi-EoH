
def heuristic(input_data):
    """
    Earliest Due Date with Machine Preference.
    Prioritizes operations with earlier due dates, uses machine preference.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    schedule = {}
    job_due_dates = {} #assign random due date to jobs

    for job in range(1, n_jobs + 1):
        job_due_dates[job] = sum(sum(times) for machines, times in jobs_data[job])

    # Sort jobs by due date
    sorted_jobs = sorted(jobs_data.keys(), key=lambda job: job_due_dates[job])

    for job in sorted_jobs:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs_data[job]):
            op_num = op_idx + 1
            available_machines, processing_times = operation

            #Machine preference: find machine with min available time
            best_machine = None
            min_end_time = float('inf')

            for machine_idx, machine in enumerate(available_machines):
                processing_time = processing_times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job] = best_start_time + best_processing_time

    return schedule
