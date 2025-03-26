
def heuristic(input_data):
    """Schedules jobs dynamically balancing makespan, separation, and machine load."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_op_idx = {j: 0 for j in jobs}

    scheduled_count = 0
    total_operations = sum(len(ops) for ops in jobs.values())

    while scheduled_count < total_operations:
        eligible_operations = []
        for job_id, op_idx in job_op_idx.items():
            if op_idx < len(jobs[job_id]):
                eligible_operations.append((job_id, op_idx))

        if not eligible_operations:
            break

        best_op = None
        best_machine = None
        best_start_time = float('inf')
        best_end_time = float('inf')

        for job_id, op_idx in eligible_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + time

                # Dynamic priority: favors shorter jobs and less loaded machines
                priority = time + machine_available_times[machine] / (sum(len(op) for op in jobs[job_id]))

                if end_time < best_end_time or (end_time == best_end_time and priority < float('inf')):

                    best_op = (job_id, op_idx)
                    best_machine = machine
                    best_start_time = start_time
                    best_end_time = end_time
                    best_time = time

        if best_op is not None:
            job_id, op_idx = best_op
            op_num = op_idx + 1

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_end_time,
                'Processing Time': best_time
            })

            machine_available_times[best_machine] = best_end_time
            job_completion_times[job_id] = best_end_time
            job_op_idx[job_id] += 1
            scheduled_count += 1

    return schedule
