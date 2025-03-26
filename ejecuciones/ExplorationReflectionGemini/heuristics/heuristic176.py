
def heuristic(input_data):
    """Prioritizes shortest processing time operations."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times, job))

    def calculate_priority(job, op_idx, machines, times):
        min_time = min(times)
        return min_time

    operations.sort(key=lambda x: calculate_priority(x[4], x[1], x[2], x[3]))

    for job, op_idx, machines, times, original_job in operations:
        op_num = op_idx + 1
        best_machine = None
        min_end_time = float('inf')
        processing_time = None

        for i, machine in enumerate(machines):
            start_time = max(machine_time[machine], job_completion_time[original_job])
            end_time = start_time + times[i]

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = times[i]

        start_time = max(machine_time[best_machine], job_completion_time[original_job])
        end_time = start_time + processing_time

        schedule[original_job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_time[best_machine] = end_time
        job_completion_time[original_job] = end_time

    return schedule
