
def heuristic(input_data):
    """Schedules jobs considering machine load and job sequence."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}

    # Prioritize jobs with more operations (Longest Processing Time variant)
    job_priorities = sorted(jobs.keys(), key=lambda job_id: len(jobs[job_id]), reverse=True)


    for job_id in job_priorities:
        schedule[job_id] = []
        ops = jobs[job_id]
        current_job_time = job_completion_times[job_id] # Initialize the job time.

        for op_idx, (machines, times) in enumerate(ops):
            op_num = op_idx + 1

            # Find the best machine based on earliest availability.
            best_machine, best_time, earliest_start = None, float('inf'), float('inf')

            for m_idx, machine in enumerate(machines):
                time = times[m_idx]
                available_time = machine_available_times[machine]
                start_time = max(available_time, current_job_time)

                if start_time < earliest_start:
                    earliest_start = start_time
                    best_machine = machine
                    best_time = time

            # Schedule the operation on the best machine.
            start_time = max(machine_available_times[best_machine], current_job_time)
            end_time = start_time + best_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            # Update machine and job completion times.
            machine_available_times[best_machine] = end_time
            current_job_time = end_time
            job_completion_times[job_id] = end_time
    return schedule
