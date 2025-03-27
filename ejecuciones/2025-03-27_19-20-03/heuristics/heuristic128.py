
def heuristic(input_data):
    """Schedules jobs by earliest due date (EDD) and shortest processing time (SPT)."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_due_dates = {}

    # Calculate job due dates (sum of min processing times for each job).
    for job, operations in jobs_data.items():
        job_due_dates[job] = sum(min(times) for _, times in operations)

    # Sort jobs by due date (earliest first).
    job_order = sorted(job_due_dates.keys(), key=job_due_dates.get)

    for job in job_order:
        schedule[job] = []
        current_time = 0

        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1

            # Find the machine with shortest processing time available.
            best_machine = None
            min_processing_time = float('inf')
            chosen_processing_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                available_time = machine_available_time[machine]
                if processing_time < min_processing_time:
                    min_processing_time = processing_time
                    best_machine = machine
                    chosen_processing_time = processing_time

            # Schedule operation on chosen machine.
            start_time = max(machine_available_time[best_machine], current_time)
            processing_time = chosen_processing_time
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine available time and job completion time.
            machine_available_time[best_machine] = end_time
            current_time = end_time
            job_completion_time[job] = end_time

    return schedule
