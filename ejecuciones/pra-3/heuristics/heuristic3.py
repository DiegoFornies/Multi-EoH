
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes jobs with shorter total processing times
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
            total_time += min(times)  # Assuming we want to pick the shortest possible time.
        job_processing_times[job] = total_time

    # Sort jobs based on total processing time (shortest first)
    sorted_jobs = sorted(job_processing_times.items(), key=lambda item: item[1])
    sorted_jobs = [job for job, _ in sorted_jobs]

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs_data}
    schedule = {}

    for job in sorted_jobs:
        schedule[job] = []
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1

            # Find the machine with the earliest available time among feasible machines
            best_machine = None
            best_start_time = float('inf')
            best_processing_time = None

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job])

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule the operation on the selected machine
            start_time = best_start_time
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine available time and job completion time
            machine_available_times[best_machine] = end_time
            job_completion_times[job] = end_time

    return schedule
