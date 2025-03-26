
def heuristic(input_data):
    """Adaptive heuristic combining SPT and load balancing."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)} # Track machine load
    schedule = {j: [] for j in jobs}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        # Adaptive priority: SPT + Load Balancing
        best_op = None
        best_score = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Find the machine with the earliest available time, considering machine load
            best_machine = None
            best_start_time = float('inf')
            best_time = None

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_time = time

            # Score = normalized processing time + normalized machine load
            normalized_time = best_time #/ sum(times) if sum(times)>0 else 0
            normalized_load = machine_load[best_machine] #/ sum(machine_load.values()) if sum(machine_load.values())>0 else 0

            score = normalized_time + normalized_load
            if score < best_score:
                best_score = score
                best_op = op_data
                selected_machine = best_machine
                selected_time = best_time


        # Schedule the best operation
        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        start_time = max(machine_available_times[selected_machine], job_completion_times[job_id])
        end_time = start_time + selected_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': selected_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': selected_time
        })

        # Update machine availability, job completion time, and machine load
        machine_available_times[selected_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_load[selected_machine] += selected_time

        # Remove the scheduled operation and add the next one (if any)
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
