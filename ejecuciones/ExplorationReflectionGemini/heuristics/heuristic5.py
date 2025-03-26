
def heuristic(input_data):
    """Schedules jobs using a shortest processing time and earliest start time heuristic."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}

    # Prioritize operations based on SPT (Shortest Processing Time) and EST (Earliest Start Time).
    operations_queue = []
    for job_id, operations in jobs.items():
        for op_idx, op_data in enumerate(operations):
            machines, times = op_data
            min_time = min(times)  # Use shortest processing time to prioritize operations
            operations_queue.append((min_time, job_id, op_idx))

    operations_queue.sort()  # Sort the queue by processing time.

    for _, job_id, op_idx in operations_queue:
        machines, times = jobs[job_id][op_idx]

        # Find the machine that allows the earliest start time for this operation.
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the selected machine.
        end_time = best_start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine available time and job completion time.
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
