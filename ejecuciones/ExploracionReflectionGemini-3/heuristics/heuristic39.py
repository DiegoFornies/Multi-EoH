
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes jobs with fewer operations and shorter processing times."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Calculate a priority score for each job based on number of operations and total processing time
    job_priorities = {}
    for job_id, operations in jobs.items():
        total_processing_time = sum(min(op[1]) for op in operations) # min processing time if multiple machines available
        job_priorities[job_id] = len(operations) + (total_processing_time / 100.0)  # Higher priority if fewer ops and shorter time

    # Sort jobs by priority (lower score = higher priority)
    sorted_job_ids = sorted(job_priorities.keys(), key=lambda job_id: job_priorities[job_id])

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job_id: 0 for job_id in jobs}

    for job_id in sorted_job_ids:
        schedule[job_id] = []
        for op_idx, (machines, times) in enumerate(jobs[job_id]):
            op_num = op_idx + 1
            best_machine, best_time = -1, float('inf')
            
            # Find the machine that minimizes the operation's end time
            for m, t in zip(machines, times):
                start_time = max(machine_available_time[m], job_completion_time[job_id])
                end_time = start_time + t
                if end_time < best_time:
                    best_time = end_time
                    best_machine = m

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_time
            
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
