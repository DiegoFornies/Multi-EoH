
def heuristic(input_data):
    """
    Heuristic to schedule jobs on machines minimizing makespan,
    reducing idle time, and balancing machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize schedule and machine available times.
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}  # Track machine load for balancing.

    # Prioritize jobs with the most operations.
    job_priority = sorted(jobs.keys(), key=lambda job_id: len(jobs[job_id]), reverse=True)

    for job in job_priority:
        schedule[job] = []
        job_completion_time = 0  # Completion time of the last operation in the job.

        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            # Find the machine with the earliest available time and lowest load.
            best_machine, best_start_time, best_processing_time = None, float('inf'), None
            
            for m_idx, m in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[m], job_completion_time)

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = m
                    best_processing_time = processing_time
                elif start_time == best_start_time and machine_load[m] < machine_load[best_machine]:
                    best_machine = m
                    best_processing_time = processing_time
                        

            # Schedule the operation on the best machine.
            start_time = max(machine_available_time[best_machine], job_completion_time)
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job completion times and load.
            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += best_processing_time
            job_completion_time = end_time

    return schedule
