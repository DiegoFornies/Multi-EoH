
def heuristic(input_data):
    """
    Schedules jobs by prioritizing operations with shorter processing times and
    choosing machines that minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize schedule, machine availability, and job completion times.
    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}

    # Create a list of operations with job and operation indices.
    operations = []
    for job in range(1, n_jobs + 1):
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations by shortest processing time
    operations.sort(key=lambda op: min(op[3]))

    # Schedule each operation.
    for job, op_num, machines, times in operations:
        # Find the best machine for the current operation.
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            start_time = max(machine_available_time[machine], job_completion_times[job])

            if start_time < best_start_time:
                best_machine, best_start_time, best_processing_time = machine, start_time, processing_time

        # Update the schedule and machine/job completion times.
        start_time = best_start_time
        end_time = start_time + best_processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
