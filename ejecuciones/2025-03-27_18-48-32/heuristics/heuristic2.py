
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP).

    Prioritizes operations based on earliest completion time considering both machine availability and job dependencies,
    aiming to reduce makespan and improve machine utilization.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    operation_queue = []

    # Initialize the operation queue with the first operation of each job
    for job_id, operations in jobs.items():
        if operations:
            machines, times = operations[0]
            operation_queue.append((job_id, 0, machines, times))  # (job_id, op_index, machines, times)

    while operation_queue:
        # Find the operation with the earliest possible completion time
        best_op = None
        earliest_completion_time = float('inf')

        for job_id, op_index, machines, times in operation_queue:
            for machine_index, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                completion_time = start_time + times[machine_index]

                if completion_time < earliest_completion_time:
                    earliest_completion_time = completion_time
                    best_op = (job_id, op_index, machine, times[machine_index])

        # Schedule the best operation
        job_id, op_index, machine, processing_time = best_op
        start_time = max(machine_available_time[machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[machine] = end_time
        job_completion_time[job_id] = end_time

        # Remove the scheduled operation from the queue
        operation_queue.remove((job_id, op_index, jobs[job_id][op_index][0], jobs[job_id][op_index][1]))

        # Add the next operation of the job to the queue, if it exists
        next_op_index = op_index + 1
        if next_op_index < len(jobs[job_id]):
            machines, times = jobs[job_id][next_op_index]
            operation_queue.append((job_id, next_op_index, machines, times))

    return schedule
