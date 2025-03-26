
def heuristic(input_data):
    """Schedules jobs considering machine load and shortest processing time."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)} # Track machine load

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        # Prioritize based on processing time, machine load, and earliest start
        best_op = None
        best_start_time = float('inf')
        best_load_score = float('inf')  # Lower is better

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            earliest_start_time = float('inf')
            selected_machine = None
            selected_time = None

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])

                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    selected_machine = machine
                    selected_time = time

            # Calculate machine load score.  Prefer lightly loaded machines.
            load_score = machine_load[selected_machine]
            
            if earliest_start_time < best_start_time or \
               (earliest_start_time == best_start_time and load_score < best_load_score):
                best_start_time = earliest_start_time
                best_load_score = load_score
                best_op = op_data
                best_machine = selected_machine
                best_time = selected_time

        # Schedule the best operation
        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine availability, job completion, and machine load
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_load[best_machine] += best_time # Increase machine load

        # Remove scheduled operation and add the next (if any)
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
