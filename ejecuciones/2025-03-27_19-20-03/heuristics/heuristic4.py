
def heuristic(input_data):
    """
    Heuristic scheduler that minimizes makespan by prioritizing operations
    with fewer machine options and shorter processing times.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize schedule and machine availability
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}

    # Flatten operations and add job/operation indices
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((len(machines), min(times), job, op_idx, machines, times)) # (Number of machines, shortest process time, job, operation index, available machines, process times)

    # Sort by machine availability then number of possible machines then by processing time, so that operations with fewer options are scheduled first
    operations.sort()
    # Schedule each operation
    scheduled_operations = set()
    for _, _, job, op_idx, machines, times in operations:
        job_ops = jobs_data[job]
        if (job, op_idx) in scheduled_operations:
            continue
        
        # Find the earliest available time on a suitable machine
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]

            # Ensure job sequencing constraint
            if op_idx > 0:
                prev_op_end_time = schedule[job][op_idx - 1]['End Time']
                start_time = max(machine_available_time[machine], prev_op_end_time)
            else:
                start_time = machine_available_time[machine]

            # Update best machine if earlier start is possible
            if start_time < best_start_time:
                best_machine, best_start_time, best_processing_time = machine, start_time, processing_time
        
        # Update the schedule
        if job not in schedule:
            schedule[job] = []

        end_time = best_start_time + best_processing_time
        operation_number = op_idx + 1
        schedule[job].append({
            'Operation': operation_number,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability
        machine_available_time[best_machine] = end_time
        scheduled_operations.add((job, op_idx))
    return schedule
