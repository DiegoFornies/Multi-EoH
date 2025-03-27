
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes operations based on processing time and machine availability.
    Selects the machine with the earliest available time for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of operations, sorted by shortest processing time
    operations = []
    for job, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append((job, op_idx, machines, times))

    # Flatten list to make it sortable by processing time.
    operations.sort(key=lambda x: min(x[3]))  # Sort by minimum processing time

    for job, op_idx, machines, times in operations:
        # Find the machine that can process the operation earliest.
        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            start_time = max(machine_available_times[machine], job_completion_times[job])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the selected machine
        start_time = best_start_time
        end_time = start_time + best_processing_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
