
def heuristic(input_data):
    """A heuristic for FJSSP that considers machine availability and processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize schedule, machine availability, and job completion times
    schedule = {job: [] for job in jobs}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs}

    # Sort jobs by number of operations for more efficient resource allocation
    job_order = sorted(jobs.keys(), key=lambda job: len(jobs[job]))

    for job in job_order:
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1
            best_machine, best_start_time, best_processing_time = None, float('inf'), None

            # Find the best machine to minimize start time
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_availability[machine], job_completion_times[job])

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
            
            # Schedule the operation on the best machine
            start_time = best_start_time
            end_time = start_time + best_processing_time
            schedule[job].append({'Operation': op_num, 'Assigned Machine': best_machine, 'Start Time': start_time, 'End Time': end_time, 'Processing Time': best_processing_time})

            # Update machine availability and job completion time
            machine_availability[best_machine] = end_time
            job_completion_times[job] = end_time

    return schedule
