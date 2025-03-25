
def heuristic(input_data):
    """
    A heuristic that prioritizes minimizing machine idle time
    and job completion time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of operations that are ready to be scheduled
    ready_operations = []
    for job_id, operations in jobs.items():
        ready_operations.append((job_id, 0))  # (job_id, operation_index)

    while ready_operations:
        # Select the next operation to schedule using a heuristic
        best_job, best_op_index = None, None
        earliest_end_time = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs[job_id][op_index]

            # Find the machine that allows the operation to finish earliest
            best_machine, best_time = None, None
            min_end_time = float('inf')

            for i, machine_id in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_times[machine_id], job_completion_times[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine_id
                    best_time = processing_time

            # Select the operation that can finish earliest overall
            if min_end_time < earliest_end_time:
                earliest_end_time = min_end_time
                best_job = job_id
                best_op_index = op_index
                selected_machine = best_machine
                selected_time = best_time

        # Schedule the selected operation
        start_time = max(machine_available_times[selected_machine], job_completion_times[best_job])
        end_time = start_time + selected_time

        schedule[best_job].append({
            'Operation': best_op_index + 1,
            'Assigned Machine': selected_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': selected_time
        })

        # Update machine and job completion times
        machine_available_times[selected_machine] = end_time
        job_completion_times[best_job] = end_time

        # Remove the scheduled operation from the ready list
        ready_operations.remove((best_job, best_op_index))

        # Add the next operation of the job to the ready list, if it exists
        if best_op_index + 1 < len(jobs[best_job]):
            ready_operations.append((best_job, best_op_index + 1))

    return schedule
