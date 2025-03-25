
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes operations with shortest processing time
    on available machines to minimize makespan and balance machine load.
    """
    schedule = {}
    machine_time = {m: 0 for m in range(input_data['n_machines'])}
    job_time = {j: 0 for j in input_data['jobs']}

    # Create a priority queue for operations based on processing time
    import heapq
    operation_queue = []
    for job, ops in input_data['jobs'].items():
        heapq.heappush(operation_queue, (ops[0][1][0], job, 0))  # (processing_time, job, operation_index)

    while operation_queue:
        processing_time, job, op_idx = heapq.heappop(operation_queue)
        ops = input_data['jobs'][job]
        machines, times = ops[op_idx]
        op_num = op_idx + 1

        # Find the machine with the earliest available time among feasible machines
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for i, m in enumerate(machines):
            start_time = max(machine_time[m], job_time[job])
            if start_time < best_start_time:
                best_machine = m
                best_start_time = start_time
                best_processing_time = times[i]

        # Schedule the operation on the selected machine
        start = best_start_time
        end = start + best_processing_time
        if job not in schedule:
            schedule[job] = []
        schedule[job].append({'Operation': op_num, 'Assigned Machine': best_machine, 'Start Time': start, 'End Time': end, 'Processing Time': best_processing_time})

        machine_time[best_machine] = end
        job_time[job] = end

        # Add the next operation of the same job to the queue, if any
        if op_idx + 1 < len(ops):
            heapq.heappush(operation_queue, (ops[op_idx + 1][1][0], job, op_idx + 1))

    return schedule
