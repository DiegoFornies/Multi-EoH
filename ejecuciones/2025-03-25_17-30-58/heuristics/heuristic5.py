
def heuristic(input_data):
    """A heuristic for the FJSSP that prioritizes minimizing idle time on machines."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize data structures
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Iterate through jobs
    for job_id in jobs:
        schedule[job_id] = []
        operations = jobs[job_id]

        # Iterate through operations in the job
        for op_idx, operation in enumerate(operations):
            machines = operation[0]
            processing_times = operation[1]

            # Find the machine with the earliest available time that can perform the operation
            best_machine = None
            min_available_time = float('inf')

            for machine_idx, machine in enumerate(machines):
                available_time = max(machine_available_time[machine], job_completion_time[job_id])
                if available_time < min_available_time:
                    min_available_time = available_time
                    best_machine = machine
                    best_processing_time = processing_times[machine_idx]

            # Schedule the operation on the best machine
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job completion times
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
