
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP)
    that considers machine load balancing and job completion time.

    It iterates through jobs and operations, assigning each operation
    to the machine with the earliest available time, while considering
    the job's precedence constraints.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}  # Store the schedule for each job
    machine_available_time = {m: 0 for m in range(n_machines)}  # Earliest available time for each machine
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Completion time of each job

    for job_id, operations in jobs.items():
        schedule[job_id] = []
        for op_idx, operation in enumerate(operations):
            machines, processing_times = operation

            # Find the machine that allows the earliest operation start
            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None

            for machine, processing_time in zip(machines, processing_times):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule the operation on the selected machine
            start_time = min_start_time
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine available time and job completion time
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
