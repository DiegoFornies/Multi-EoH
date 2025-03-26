
def heuristic(input_data):
    """Combines SPT and load balancing adaptively."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    operation_queue = []

    # Initialize operation queue
    for job, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            operation_queue.append((job, op_idx))

    while operation_queue:
        best_op = None
        best_machine = None
        min_completion_time = float('inf')

        for job, op_idx in list(operation_queue):
            machines, times = jobs[job][op_idx]
            op_num = op_idx + 1

            # SPT component: prefer shorter processing times
            min_time_option = float('inf')
            available_machines_options = []
            for idx, machine in enumerate(machines):
                available_machines_options.append((machine, times[idx]))
                min_time_option = min(min_time_option, times[idx])

            for i, m in enumerate(machines):
                # Load balancing component: consider machine load
                start_time = max(machine_time[m], job_completion_time[job])
                end_time = start_time + times[i]
                completion_time = end_time + 0.01 * machine_time[m]  # Bias towards low machine_time

                # Adaptive: Combine SPT and load balancing
                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_op = (job, op_idx)
                    best_machine = m

        if best_op is not None:
            job, op_idx = best_op
            machines, times = jobs[job][op_idx]
            processing_time = times[machines.index(best_machine)]
            op_num = op_idx + 1

            start_time = max(machine_time[best_machine], job_completion_time[job])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_time[best_machine] = end_time
            job_completion_time[job] = end_time
            operation_queue.remove((job, op_idx))

    return schedule
