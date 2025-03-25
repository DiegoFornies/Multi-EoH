
def heuristic(input_data):
    """A heuristic for FJSSP that considers machine availability and job precedence."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize data structures
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    # Iterate through all operations of each job
    for job_id in jobs:
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            op_num = op_idx + 1

            # Find the earliest available machine that can perform the operation
            best_machine = None
            min_start_time = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule the operation on the best machine
            start_time = min_start_time
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine available time and job completion time
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
