
def heuristic(input_data):
    """Schedules jobs using a priority rule based on operation slack."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    job_order = list(jobs_data.keys())  # Consider jobs in original order

    for job in job_order:
        schedule[job] = []
        current_time = 0

        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1

            # Calculate slack for each possible machine assignment
            machine_slack = {}
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], current_time)
                slack = start_time + processing_time  # Smaller slack is better
                machine_slack[machine] = slack

            # Choose the machine with smallest slack.
            best_machine = min(machine_slack, key=machine_slack.get)

            # Find processing time based on machine selection
            m_idx = machines.index(best_machine)
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

            # Update machine available time and job completion time.
            machine_available_time[best_machine] = end_time
            current_time = end_time
            job_completion_time[job] = end_time

    return schedule
