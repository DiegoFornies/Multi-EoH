
def heuristic(input_data):
    """
    Heuristic scheduling algorithm for FJSSP.
    Prioritizes jobs with shortest processing time (SPT) and selects machines based on earliest availability.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Calculate total processing time for each job
    job_processing_times = {}
    for job, operations in jobs_data.items():
        total_time = sum(min(times) for machines, times in operations)  # Minimum time if multiple options
        job_processing_times[job] = total_time

    # Sort jobs by shortest processing time
    sorted_jobs = sorted(job_processing_times.items(), key=lambda item: item[1])

    # Initialize machine availability times
    machine_availability = {m: 0 for m in range(n_machines)}
    schedule = {}

    for job_id, _ in sorted_jobs:
        job_schedule = []
        current_time = 0

        for op_idx, operation in enumerate(jobs_data[job_id]):
            machines, times = operation
            op_num = op_idx + 1

            # Find the machine with the earliest availability among feasible machines
            best_machine = None
            best_time = float('inf')
            best_processing_time = None

            for i, machine in enumerate(machines):
                if machine_availability[machine] < best_time:
                    best_time = machine_availability[machine]
                    best_machine = machine
                    best_processing_time = times[i]

            # Schedule the operation on the selected machine
            start_time = max(current_time, machine_availability[best_machine])
            end_time = start_time + best_processing_time

            job_schedule.append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability and current job time
            machine_availability[best_machine] = end_time
            current_time = end_time

        schedule[job_id] = job_schedule

    return schedule
