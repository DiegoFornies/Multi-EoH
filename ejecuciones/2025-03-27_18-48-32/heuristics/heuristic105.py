
def heuristic(input_data):
    """FJSSP heuristic: Shortest Processing Time & earliest start."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times, job))

        # Sort by shortest processing time among all possible machines and earliest start time
        eligible_operations.sort(key=lambda x: min([(x[3][i], max(machine_available_time[x[2][i]], job_completion_time[x[4]])) for i in range(len(x[2]))]))

        job, op_num, machines, times, original_job = eligible_operations[0]

        best_machine = None
        min_end_time = float('inf')

        for m_idx, m in enumerate(machines):
            start_time = max(machine_available_time[m], job_completion_time[job])
            end_time = start_time + times[m_idx]
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = m
                best_start_time = start_time
                best_processing_time = times[m_idx]

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job] = best_start_time + best_processing_time

        remaining_operations[job].pop(0)

    return schedule
