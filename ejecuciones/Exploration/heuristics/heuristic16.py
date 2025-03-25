
def heuristic(input_data):
    """A heuristic for FJSSP minimizing makespan and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}

    # Sort operations by shortest processing time for any machine.
    operation_queue = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            min_time = min(times)
            operation_queue.append((min_time, job_id, op_idx))

    operation_queue.sort()

    for _, job_id, op_idx in operation_queue:
        machines, times = jobs[job_id][op_idx]
        
        best_machine = -1
        min_end_time = float('inf')
        best_processing_time = -1

        # Find the machine that results in the earliest completion time, considering both
        # machine availability and job completion time.
        for i in range(len(machines)):
            machine = machines[i]
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the best machine
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

        # Update machine availability and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
