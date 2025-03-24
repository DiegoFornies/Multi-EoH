
def heuristic(input_data):
    """
    A heuristic to solve the Flexible Job Shop Scheduling Problem (FJSSP).
    The heuristic prioritizes operations with fewer machine choices.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize schedule, machine availability times, and job completion times
    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_availability = {machine: 0 for machine in range(1, n_machines + 1)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}

    # Create a list of operations with their job and operation number
    operations = []
    for job, operations_list in jobs_data.items():
        for op_idx, op_data in enumerate(operations_list):
            operations.append((job, op_idx + 1, op_data))

    # Sort operations by the number of available machines in ascending order
    operations.sort(key=lambda x: len(x[2][0]))

    # Schedule operations
    for job, op_num, op_data in operations:
        machines, times = op_data

        # Find the earliest available time slot on a suitable machine
        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for machine, time in zip(machines, times):
            start_time = max(machine_availability[machine], job_completion_times[job])
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = time

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

        # Update machine availability and job completion time
        machine_availability[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
