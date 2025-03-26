
def heuristic(input_data):
    """Prioritize operations by shortest processing time; balance machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    operation_queue = []

    # Create operation queue, prioritize shortest processing time
    for job, operations in jobs.items():
        for op_num, (machines, times) in enumerate(operations):
            min_time = min(times)
            operation_queue.append((min_time, job, op_num, machines, times))
    operation_queue.sort()

    for _, job, op_num, machines, times in operation_queue:
        best_machine, min_end_time, processing_time = None, float('inf'), None

        for i, m in enumerate(machines):
            start_time = max(job_completion_times[job], machine_load[m])
            end_time = start_time + times[i]
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = m
                processing_time = times[i]
        
        start_time = max(job_completion_times[job], machine_load[best_machine])
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_num + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_load[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
