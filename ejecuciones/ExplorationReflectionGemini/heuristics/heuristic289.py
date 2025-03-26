
def heuristic(input_data):
    """Schedules jobs with SPT and Job Urgency."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        best_op = None
        best_score = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Find the earliest possible start time and machine
            best_machine = None
            earliest_start_time = float('inf')
            selected_time = None
            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    selected_time = time

            # Job Urgency: time remaining for the job
            remaining_time = 0
            for i in range(op_idx + 1, len(jobs[job_id])):
                remaining_time += min(jobs[job_id][i][1])

            score = 0.4 * (earliest_start_time + selected_time) + 0.6*remaining_time

            if score < best_score:
                best_score = score
                best_op = op_data
                chosen_machine = best_machine
                chosen_time = selected_time
                start_select = earliest_start_time

        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        start_time = max(machine_available_times[chosen_machine], job_completion_times[job_id])
        end_time = start_time + chosen_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': chosen_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': chosen_time
        })

        machine_available_times[chosen_machine] = end_time
        job_completion_times[job_id] = end_time

        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
