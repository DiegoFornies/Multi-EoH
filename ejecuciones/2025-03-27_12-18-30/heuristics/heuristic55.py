
def heuristic(input_data):
    """Schedules jobs balancing earliest start and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []

        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            best_machine = None
            earliest_start_time = float('inf')
            best_processing_time = None
            min_load_time = float('inf')
            #Chooses machine with earliest available time, breaking ties by choosing the machine with the smallest processing time
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])

                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
                    min_load_time = machine_available_time[machine] + processing_time
                elif start_time == earliest_start_time and (machine_available_time[machine] + processing_time) < min_load_time:
                    best_machine = machine
                    best_processing_time = processing_time
                    min_load_time = machine_available_time[machine] + processing_time
            start_time = max(machine_available_time[best_machine], job_completion_time[job])
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
