
def heuristic(input_data):
    """
    A heuristic for the FJSSP that considers machine load and job completion time.
    Prioritizes machines with earlier available times to balance load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}  # Stores the schedule for each job
    machine_available_time = {m: 0 for m in range(n_machines)}  # Tracks when each machine is available
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}  # Tracks when each job is complete

    for job_id, operations in jobs.items():
        schedule[job_id] = []
        for op_index, operation in enumerate(operations):
            machines = operation[0]
            processing_times = operation[1]

            # Find the machine that minimizes the completion time of the operation
            best_machine = None
            min_completion_time = float('inf')
            for machine_index, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                completion_time = start_time + processing_times[machine_index]

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine
                    best_processing_time = processing_times[machine_index]

            # Schedule the operation on the chosen machine
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability and job completion time
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
