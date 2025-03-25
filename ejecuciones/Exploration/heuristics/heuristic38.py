
def heuristic(input_data):
    """Heuristic scheduling algorithm for FJSSP.
    It prioritizes jobs based on shortest total processing time
    and assigns operations to machines with the earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Calculate total processing time for each job
    job_processing_times = {}
    for job, operations in jobs_data.items():
        total_time = 0
        for machines, times in operations:
            total_time += min(times)  # Consider the minimum processing time if multiple machines
        job_processing_times[job] = total_time

    # Sort jobs based on total processing time (shortest first)
    sorted_jobs = sorted(job_processing_times.items(), key=lambda item: item[1])
    sorted_jobs = [job for job, _ in sorted_jobs]

    # Initialize machine availability times
    machine_availability = {m: 0 for m in range(1, n_machines + 1)}

    # Initialize schedule
    schedule = {}

    for job in sorted_jobs:
        schedule[job] = []
        job_completion_time = 0

        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1
            best_machine, best_time = None, float('inf')
            
            # Find the best machine for the current operation
            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                available_time = machine_availability[machine]
                start_time = max(available_time, job_completion_time)
                
                if start_time + time < best_time:
                    best_time = start_time + time
                    best_machine = machine
                    best_processing_time = time
                    best_start_time = start_time

            # Assign the operation to the best machine
            start_time = best_start_time
            end_time = best_time
            assigned_machine = best_machine

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': assigned_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability and job completion time
            machine_availability[assigned_machine] = end_time
            job_completion_time = end_time

    return schedule
