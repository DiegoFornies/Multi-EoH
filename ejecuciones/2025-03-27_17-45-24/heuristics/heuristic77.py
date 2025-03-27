
def heuristic(input_data):
    """Schedules jobs based on Shortest Processing Time (SPT) and earliest available machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Flatten operations to sort by processing time
    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_index, (machines, times) in enumerate(jobs_data[job_id]):
            operations.append((job_id, op_index, machines, times))

    # Sort operations by shortest processing time
    operations.sort(key=lambda x: min(x[3]))  # Sort by minimum processing time

    for job_id, op_index, machines, times in operations:
        # Find the machine with earliest available time for this operation
        best_machine = None
        earliest_start_time = float('inf')
        processing_time = None

        for m_index, machine in enumerate(machines):
            start_time = max(machine_available_time[machine],
                            schedule[job_id][-1]['End Time'] if op_index > 0 and schedule[job_id] else 0)
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                processing_time = times[m_index]

        # Schedule the operation on the selected machine
        start_time = earliest_start_time
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine available time
        machine_available_time[best_machine] = end_time

    return schedule
