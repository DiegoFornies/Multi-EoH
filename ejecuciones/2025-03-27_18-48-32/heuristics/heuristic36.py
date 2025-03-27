
def heuristic(input_data):
    """Schedules jobs by balancing machine workload and minimizing idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}

    operations_list = []
    for job, operations in jobs_data.items():
        for op_num in range(1, len(operations) + 1):
            operations_list.append((job, op_num))

    while operations_list:
        best_op = None
        best_machine = None
        min_increase = float('inf')

        for job, op_num in operations_list:
            machines, times = jobs_data[job][op_num - 1]
            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_times[job])
                increase = times[m_idx] # machine_load[m]
                if increase < min_increase:
                    min_increase = increase
                    best_op = op_num
                    best_machine = m
                    best_time = times[m_idx]
                    best_job = job

        start_time = max(machine_available_times[best_machine], job_completion_times[best_job])
        end_time = start_time + best_time
        scheduled_operations[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_times[best_machine] = end_time
        machine_load[best_machine] += best_time
        job_completion_times[best_job] = end_time
        operations_list.remove((best_job, best_op))

    return scheduled_operations
