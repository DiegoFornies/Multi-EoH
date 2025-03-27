
def heuristic(input_data):
    """Balances makespan and machine load using adaptive urgency and load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 1))

    while eligible_operations:
        best_op = None
        earliest_start = float('inf')
        best_machine = None
        best_time = None
        best_job = None

        for job, op_num in eligible_operations:
            machines, times = jobs_data[job][op_num - 1]

            best_local_machine = None
            best_local_start = float('inf')
            best_local_time = None

            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_times[job])

                load_penalty = machine_load[m] * 0.05
                remaining_ops = len(jobs_data[job]) - op_num + 1
                urgency_factor = max(0, 1 - remaining_ops / len(jobs_data[job]))
                load_penalty *= (1 - urgency_factor)
                
                adjusted_start_time = start_time + load_penalty

                if adjusted_start_time < best_local_start:
                    best_local_start = adjusted_start_time
                    best_local_machine = m
                    best_local_time = times[m_idx]

            if best_local_start < earliest_start:
                earliest_start = best_local_start
                best_op = op_num
                best_machine = best_local_machine
                best_time = best_local_time
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
        job_completion_times[best_job] = end_time
        machine_load[best_machine] += best_time

        eligible_operations.remove((best_job, best_op))

        if best_op < len(jobs_data[best_job]):
            eligible_operations.append((best_job, best_op + 1))

    return scheduled_operations
