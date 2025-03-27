
def heuristic(input_data):
    """
    A heuristic for FJSSP minimizing makespan by assigning each operation to the earliest available machine and time slot.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}  # When each machine is next available
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}  # When each job is completed

    schedule = {}
    for job in range(1, n_jobs + 1):
        schedule[job] = []

    # Create a list of operations to schedule, sorted by shortest processing time
    operations_to_schedule = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations_to_schedule.append((job, op_idx, machines, times))

    operations_to_schedule.sort(key=lambda x: min(x[3]))  # Sort by shortest processing time

    for job, op_idx, machines, times in operations_to_schedule:
        min_start_time = float('inf')
        best_machine = None
        best_processing_time = None

        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]

            start_time = max(machine_available_times[machine], job_completion_times[job])

            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        start_time = min_start_time
        end_time = start_time + best_processing_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
