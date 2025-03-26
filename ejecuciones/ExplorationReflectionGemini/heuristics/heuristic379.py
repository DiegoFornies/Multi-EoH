
def heuristic(input_data):
    """Schedules jobs considering machine load and job dependencies."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    operation_queue = []

    # Initialize operation queue with first operation of each job
    for job_id in jobs:
        operation_queue.append((job_id, 0)) # (job_id, operation_index)

    while operation_queue:
        # Prioritize operations based on machine load and shortest processing time
        best_job = None
        best_op_idx = None
        best_machine = None
        min_completion_time = float('inf')

        for job_id, op_idx in operation_queue:
            possible_machines, possible_times = jobs[job_id][op_idx]
            for machine, time in zip(possible_machines, possible_times):
                # Calculate the potential completion time on each machine
                start_time = max(machine_load[machine], job_completion_times[job_id])
                completion_time = start_time + time

                # Select the operation with the earliest completion time (considering current load)
                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_job = job_id
                    best_op_idx = op_idx
                    best_machine = machine
                    best_time = time
                    start = start_time

        # Schedule the selected operation
        operation_queue.remove((best_job, best_op_idx))
        op_num = best_op_idx + 1
        end_time = start + best_time

        schedule[best_job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine load and job completion time
        machine_load[best_machine] = end_time
        job_completion_times[best_job] = end_time

        # Add the next operation of the job to the queue, if it exists
        next_op_idx = best_op_idx + 1
        if next_op_idx < len(jobs[best_job]):
            operation_queue.append((best_job, next_op_idx))

    return schedule
