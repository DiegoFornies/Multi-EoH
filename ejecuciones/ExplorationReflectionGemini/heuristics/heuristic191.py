
def heuristic(input_data):
    """Schedules jobs using a dynamic SPT and load balancing heuristic."""
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
            best_time = float('inf')
            earliest_start_time = float('inf')

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    best_time = time

            # Dynamic weight adjustment based on machine load
            machine_load = machine_available_times[best_machine]
            processing_time = best_time
            load_ratio = machine_load / (sum(machine_available_times.values()) / n_machines + 1e-9) #Avoid dividing zero
            weight_spt = 0.8 - min(0.5, load_ratio) #Heavier load means more reliance on SPT
            weight_load = 1 - weight_spt

            # Combine SPT and load balancing
            score = weight_spt * (earliest_start_time + processing_time) + weight_load * machine_load

            if score < best_score:
                best_score = score
                best_op = op_data
                selected_machine = best_machine
                selected_time = best_time
                start_time_select = earliest_start_time

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

        # Update machine availability and job completion time
        machine_available_times[selected_machine] = end_time
        job_completion_times[job_id] = end_time

        # Remove the scheduled operation and add the next one
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
