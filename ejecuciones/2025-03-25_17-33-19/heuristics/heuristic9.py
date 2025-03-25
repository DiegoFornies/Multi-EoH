
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) that prioritizes
    minimizing idle time and balancing machine load based on processing time and
    machine availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in jobs}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}

    operations_queue = []
    for job, operations in jobs.items():
        operations_queue.append((job, 0))  # (job_id, operation_index)

    while operations_queue:
        # Sort operations by shortest processing time first, then by earliest job completion time
        operations_queue.sort(key=lambda x: (
            min(input_data['jobs'][x[0]][x[1]][1]),  # Shortest processing time for the operation
            job_completion_time[x[0]] #earliest job completion time
        ))

        job_id, operation_index = operations_queue.pop(0)
        machines, times = jobs[job_id][operation_index]

        # Find the machine with the earliest available time for the current operation
        best_machine, best_time, min_start_time = None, float('inf'), float('inf')
        for i in range(len(machines)):
            machine, time = machines[i], times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])

            if start_time < min_start_time:
                min_start_time = start_time
                best_machine, best_time = machine, time

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_time

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        # Add the next operation of the job to the queue if it exists
        if operation_index + 1 < len(jobs[job_id]):
            operations_queue.append((job_id, operation_index + 1))

    return schedule
