
def heuristic(input_data):
    """Schedules jobs considering job urgency and machine load, prioritizing critical jobs."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_remaining_work = {j: sum(min(times) for machines, times in jobs[j]) for j in jobs}  # Estimated remaining work
    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        # Prioritize operations based on job urgency (remaining work) and machine load
        best_op = None
        best_score = float('inf')  # Lower score is better

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Find the best machine for this operation based on machine load and processing time
            best_machine = None
            best_time = float('inf')
            earliest_start = float('inf')

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                if start_time < earliest_start or (start_time == earliest_start and time < best_time):
                    earliest_start = start_time
                    best_machine = machine
                    best_time = time

            # Calculate a score based on job urgency and machine load
            job_urgency = job_remaining_work[job_id]
            machine_load = machine_available_times[best_machine]
            score = job_urgency + machine_load  # Prioritize urgent jobs and less loaded machines

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

        # Update machine availability, job completion time, and remaining work
        machine_available_times[selected_machine] = end_time
        job_completion_times[job_id] = end_time
        job_remaining_work[job_id] -= min(times for mach, times in [([selected_machine], [selected_time])])  # Update remaining work based on min time

        # Remove the scheduled operation from available operations and add the next operation (if any)
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
