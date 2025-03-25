
def heuristic(input_data):
    """A heuristic for FJSSP that minimizes makespan, idle time, and balances machine load using shortest processing time (SPT) and earliest start time (EST) rules."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Prioritize operations based on Shortest Processing Time (SPT) within each job
    operation_queue = []
    for job_id, operations in jobs.items():
        for op_idx, op_data in enumerate(operations):
            machines, times = op_data
            min_time_idx = times.index(min(times))  # Find the shortest processing time
            operation_queue.append((job_id, op_idx + 1, machines[min_time_idx], times[min_time_idx]))

    # Sort operations by shortest processing time, earliest start time
    operation_queue.sort(key=lambda x: x[3]) #sorts by processing time

    for job_id, op_num, machine, processing_time in operation_queue:
        available_time_on_machine = machine_available_time[machine]
        ready_time_for_job = job_completion_time[job_id]
        start_time = max(available_time_on_machine, ready_time_for_job)
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
