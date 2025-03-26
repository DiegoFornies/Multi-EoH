
def heuristic(input_data):
    """Schedules jobs to minimize makespan, considering machine idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Sort jobs by number of operations (more operations first)
    job_priority = sorted(jobs.keys(), key=lambda j: len(jobs[j]), reverse=True)

    for job in job_priority:
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            # Find the machine that allows the earliest start time
            best_machine = None
            earliest_start_time = float('inf')
            best_processing_time = None

            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    best_processing_time = times[i]

            # Schedule the operation on the best machine
            start_time = earliest_start_time
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability and job completion time
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
