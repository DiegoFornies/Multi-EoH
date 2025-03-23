
def heuristic(input_data):
    """
    Heuristic for FJSSP scheduling. Sorts operations by shortest processing time, 
    then assigns each operation to the earliest available machine based on the minimum end time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize schedule and machine available times
    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}

    # Flatten operations and sort by shortest processing time
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    operations.sort(key=lambda x: min(x[3])) # Sort operations by min processing time

    for job, op_num, machines, times in operations:
        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        # Find the earliest available machine for the current operation
        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the best machine
        end_time = best_start_time + best_processing_time
        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine available time and job completion time
        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
