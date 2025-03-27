
def heuristic(input_data):
    """Schedules jobs using EDD and SPT to minimize makespan."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_processing_times = {}

    # Calculate total processing time for each job for EDD.
    for job, operations in jobs_data.items():
        total_time = sum(min(times) for machines, times in operations)
        job_processing_times[job] = total_time

    # Sort jobs based on EDD (Earliest Due Date, approximated by total processing time).
    job_order = sorted(jobs_data.keys(), key=lambda job: job_processing_times[job])

    for job in job_order:
        schedule[job] = []
        current_time = 0

        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1
            best_machine = None
            min_end_time = float('inf')
            processing_time = None

            # SPT (Shortest Processing Time) for machine assignment.
            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], current_time)
                end_time = start_time + times[m_idx]
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    processing_time = times[m_idx]

            start_time = max(machine_available_time[best_machine], current_time)
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            current_time = end_time

    return schedule
