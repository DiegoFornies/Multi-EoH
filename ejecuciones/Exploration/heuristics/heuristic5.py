
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes minimizing idle time and balancing machine load."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize schedule and machine availability times
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}

    # Initialize job completion times
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Iterate through jobs and operations
    for job_id in sorted(jobs.keys()):
        schedule[job_id] = []
        ops = jobs[job_id]

        for op_idx, op in enumerate(ops):
            machines, times = op

            # Find the machine with the earliest available time
            best_machine = None
            min_start_time = float('inf')

            for m_idx, machine in enumerate(machines):
                # Consider both machine availability and job completion time
                start_time = max(machine_available_time[machine], job_completion_times[job_id])
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_time = times[m_idx]
            
            # Schedule the operation on the best machine
            start_time = max(machine_available_time[best_machine], job_completion_times[job_id])
            end_time = start_time + best_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })
            
            # Update machine availability time and job completion time
            machine_available_time[best_machine] = end_time
            job_completion_times[job_id] = end_time
    
    return schedule
