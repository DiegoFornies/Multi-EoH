
def heuristic(input_data):
    """Schedules jobs using a dynamic priority rule considering makespan, machine load, and job dependencies."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_starts = {j: 0 for j in jobs}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        # Prioritize operations dynamically
        best_op = None
        best_score = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            best_machine = None
            best_time = float('inf')
            earliest_start = float('inf')

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_machine = machine
                    best_time = time
            
            # Calculate a score based on makespan and machine load balancing
            makespan_penalty = 1.0  # Adjust for makespan importance
            load_penalty = 0.5      # Adjust for load balancing importance
            dependency_bonus = 0.2

            makespan_impact = earliest_start + best_time
            machine_load = machine_available_times[best_machine]
            # Prioritize earlier jobs
            dependency = job_starts[job_id]

            score = makespan_penalty * makespan_impact + load_penalty * machine_load - dependency_bonus*dependency

            if score < best_score:
                best_score = score
                best_op = op_data
                selected_machine = best_machine
                selected_time = best_time
                start_time = earliest_start

        # Schedule the best operation
        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

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
        if(op_idx==0):
          job_starts[job_id] = start_time

        # Remove the scheduled operation from available operations and add the next operation (if any)
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
