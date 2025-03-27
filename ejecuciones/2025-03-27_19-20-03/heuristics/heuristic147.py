
def heuristic(input_data):
    """Schedules jobs using a modified Shortest Remaining Processing Time (SRPT) approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_remaining_times = {}

    for job, operations in jobs_data.items():
        total_time = sum(min(times) for machines, times in operations)
        job_remaining_times[job] = total_time

    scheduled_operations = {}  # Track operations already scheduled for each job

    for job in jobs_data:
        scheduled_operations[job] = []
        schedule[job] = []

    current_time = 0
    while True:
        eligible_jobs = []
        for job in jobs_data:
            next_op_index = len(scheduled_operations[job])
            if next_op_index < len(jobs_data[job]):
                eligible_jobs.append(job)

        if not eligible_jobs:
            break  # All operations scheduled

        # Find job with shortest remaining processing time for the *next* operation only
        shortest_job = None
        shortest_time = float('inf')

        for job in eligible_jobs:
            next_op_index = len(scheduled_operations[job])
            machines, times = jobs_data[job][next_op_index]
            min_time = min(times)  # Shortest possible time for this operation
            if min_time < shortest_time:
                shortest_time = min_time
                shortest_job = job

        # Schedule the next operation for the shortest job
        next_op_index = len(scheduled_operations[shortest_job])
        machines, times = jobs_data[shortest_job][next_op_index]
        op_num = next_op_index + 1

        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], current_time)
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = times[m_idx]

        start_time = best_start_time
        processing_time = best_processing_time
        end_time = start_time + processing_time

        schedule[shortest_job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        scheduled_operations[shortest_job].append(op_num)  # Mark operation as scheduled
        current_time = min(machine_available_time.values())

    return schedule
