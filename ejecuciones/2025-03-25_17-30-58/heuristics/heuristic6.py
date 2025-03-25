
def heuristic(input_data):
    """A heuristic for FJSSP that considers machine load and operation urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of operations, sorted by job number and operation order
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, op))

    # Sort operations based on a priority rule (e.g., shortest processing time)
    operations.sort(key=lambda x: min(x[2][1]))  # Shortest processing time first

    for job_id, op_num, op_data in operations:
        machines, times = op_data

        # Find the machine that minimizes the completion time of the operation
        best_machine = None
        min_completion_time = float('inf')
        best_processing_time = None

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            completion_time = start_time + processing_time

            if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
