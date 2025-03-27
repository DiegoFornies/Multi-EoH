
def heuristic(input_data):
    """Schedules jobs based on shortest processing time first."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Flatten operations and sort by shortest processing time
    all_operations = []
    for job_id in range(1, n_jobs + 1):
        for op_index, operation in enumerate(jobs[job_id]):
            machines, processing_times = operation
            all_operations.append((job_id, op_index, machines, processing_times))

    # Sort operations by minimum processing time across available machines
    all_operations.sort(key=lambda x: min(x[3]))

    for job_id, op_index, machines, processing_times in all_operations:
        # Find the machine that allows the earliest operation start
        best_machine = None
        min_start_time = float('inf')
        best_processing_time = None

        for machine_index, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_processing_time = processing_times[machine_index]

        # Schedule the operation on the selected machine
        start_time = min_start_time
        end_time = start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine available time and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
