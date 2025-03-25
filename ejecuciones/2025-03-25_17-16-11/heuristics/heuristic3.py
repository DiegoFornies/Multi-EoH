
def heuristic(input_data):
    """
    A heuristic for FJSSP that minimizes makespan by prioritizing operations
    with the fewest machine options and shortest processing times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    eligible_operations = []
    for job_id, operations in jobs.items():
        eligible_operations.append((job_id, 0))

    scheduled_operations = set()

    while eligible_operations:
        # Prioritize operations based on the number of available machines
        # and shortest processing time.
        eligible_operations.sort(
            key=lambda x: (
                len(jobs[x[0]][x[1]][0]),  # Number of machines
                min(jobs[x[0]][x[1]][1]),   # Shortest processing time
            )
        )

        job_id, op_idx = eligible_operations.pop(0)
        operation = jobs[job_id][op_idx]
        machines, times = operation

        # Find the machine that allows the earliest completion time for the operation
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

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        scheduled_operations.add((job_id, op_idx))

        # Add the next operation for the job, if it exists
        next_op_idx = op_idx + 1
        if next_op_idx < len(jobs[job_id]):
            eligible_operations.append((job_id, next_op_idx))

    return schedule
