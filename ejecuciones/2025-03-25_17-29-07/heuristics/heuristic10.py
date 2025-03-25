
def heuristic(input_data):
    """A heuristic for the FJSSP that prioritizes minimizing idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}

    # Sort jobs based on total processing time (shortest first)
    job_priorities = sorted(jobs.keys(), key=lambda job: sum(min(times) for _, times in jobs[job]), reverse=False)
    
    for job in job_priorities:
        schedule[job] = []
        current_time = 0  # Job's current completion time

        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            # Find the earliest available machine for the current operation
            best_machine, best_start_time, best_processing_time = None, float('inf'), None

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_times[machine], current_time)

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule the operation on the best machine
            start_time = best_start_time
            end_time = start_time + best_processing_time
            machine_available_times[best_machine] = end_time
            current_time = end_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

        job_completion_times[job] = current_time #record job completion time
    return schedule
