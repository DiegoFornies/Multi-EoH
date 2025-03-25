
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP).
    Prioritizes operations with the shortest processing time and assigns
    them to the least loaded machine.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    available_operations = []
    for job, operations in jobs.items():
        available_operations.append((job, 0))  # (job_id, operation_index)

    completed_operations = set()
    scheduled_ops = 0
    total_ops = sum(len(ops) for ops in jobs.values())

    while scheduled_ops < total_ops:
        eligible_ops = []
        for job, op_idx in available_operations:
            if (job, op_idx) not in completed_operations:
                eligible_ops.append((job, op_idx))

        if not eligible_ops:
            break  # No more available operations

        # Find the operation with the shortest processing time among available operations
        best_op = None
        min_duration = float('inf')

        for job, op_idx in eligible_ops:
            machines, times = jobs[job][op_idx]
            shortest_time = min(times)
            if shortest_time < min_duration:
                min_duration = shortest_time
                best_op = (job, op_idx)

        job, op_idx = best_op
        machines, times = jobs[job][op_idx]

        # Find the machine with the least load among available machines for this operation
        best_machine = None
        min_load = float('inf')

        for i, machine in enumerate(machines):
            if machine_load[machine] < min_load:
                min_load = machine_load[machine]
                best_machine = machine
                best_machine_index = i
        
        processing_time = times[best_machine_index]

        start_time = max(machine_load[best_machine], job_completion_time[job])
        end_time = start_time + processing_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_load[best_machine] = end_time
        job_completion_time[job] = end_time
        completed_operations.add((job, op_idx))
        scheduled_ops += 1
        
        # Add the next operation for the job to available_operations if it exists
        if op_idx + 1 < len(jobs[job]):
            available_operations.append((job, op_idx + 1))
        

    return schedule
