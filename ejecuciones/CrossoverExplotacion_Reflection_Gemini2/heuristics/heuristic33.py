
def heuristic(input_data):
    """A heuristic for FJSSP aiming for load balancing and minimizing idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}  # Keep track of machine availability
    machine_load = {m: 0 for m in range(n_machines)}  # Track cumulative load on each machine
    job_completion_time = {j: 0 for j in jobs} # track job completion time

    schedule = {}
    for job in jobs:
        schedule[job] = []

    # Prioritize jobs with fewer operations, aiming to complete them quickly
    job_priority = sorted(jobs.keys(), key=lambda j: len(jobs[j]))

    for job in job_priority:
        job_time = 0  # Reset time for each job
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            # Choose the machine with the earliest available time, considering machine load.
            best_machine = None
            min_end_time = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_time[machine], job_completion_time[job])
                end_time = start_time + processing_time
                
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Assign the operation to the best machine
            start_time = max(machine_time[best_machine], job_completion_time[job])
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job times
            machine_time[best_machine] = end_time
            machine_load[best_machine] += best_processing_time
            job_completion_time[job] = end_time


    return schedule
