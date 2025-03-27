
def heuristic(input_data):
    """Schedules jobs minimizing makespan and machine idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    next_operation = {job: 0 for job in range(1, n_jobs + 1)}

    scheduled_count = 0
    total_operations = sum(len(ops) for ops in jobs.values())

    while scheduled_count < total_operations:
        eligible_ops = []
        for job in range(1, n_jobs + 1):
            op_idx = next_operation[job]
            if op_idx < len(jobs[job]):
                eligible_ops.append((job, op_idx))

        if not eligible_ops:
            break

        best_op = None
        best_machine = None
        min_idle = float('inf')
        best_start = None
        best_process_time = None

        for job, op_idx in eligible_ops:
            machines, times = jobs[job][op_idx]
            for m_idx, machine in enumerate(machines):
                process_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                idle_time = start_time - machine_available_time[machine] if start_time > machine_available_time[machine] else 0

                if idle_time < min_idle:
                    min_idle = idle_time
                    best_op = (job, op_idx)
                    best_machine = machine
                    best_start = start_time
                    best_process_time = process_time

        job, op_idx = best_op
        start_time = best_start

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': start_time + best_process_time,
            'Processing Time': best_process_time
        })

        machine_available_time[best_machine] = start_time + best_process_time
        job_completion_time[job] = start_time + best_process_time
        next_operation[job] += 1
        scheduled_count += 1

    return schedule
