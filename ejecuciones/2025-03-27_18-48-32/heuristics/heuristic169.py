
def heuristic(input_data):
    """Schedules jobs by Earliest Finish Time First (EFTF) rule."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                for m_idx, machine in enumerate(machines):
                    start_time = max(machine_available_time[machine], job_completion_time[job])
                    finish_time = start_time + times[m_idx]
                    eligible_operations.append((finish_time, job, op_num, machine, times[m_idx]))

        eligible_operations.sort()
        finish_time, job, op_num, best_machine, processing_time = eligible_operations[0]
        start_time = finish_time - processing_time
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': finish_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = finish_time
        job_completion_time[job] = finish_time
        remaining_operations[job].pop(0)

    return schedule
