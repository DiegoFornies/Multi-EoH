
def heuristic(input_data):
    """
    A heuristic to schedule jobs on machines, aiming to minimize makespan, separation, and balance.

    Key Idea: Shortest Processing Time (SPT) for operations, and Earliest Available Machine (EAM) selection.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}

    for job_id in jobs:
        schedule[job_id] = []

    # Flatten operations for sorting
    all_operations = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            all_operations.append((job_id, op_idx + 1, machines, times))  # (job_id, op_num, machines, times)

    # Sort operations by shortest processing time
    all_operations.sort(key=lambda op: min(op[3]))

    for job_id, op_num, machines, times in all_operations:
        # Find the earliest available machine among feasible machines
        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job_id])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the best machine
        if best_machine is not None:

            start_time = best_start_time
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine available time and job completion time
            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time
        else:
            print("No machine found for operation.")

    return schedule
