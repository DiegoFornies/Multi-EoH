
def heuristic(input_data):
    """Schedules jobs using a least work remaining (LWR) and random machine selection"""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    remaining_work = {}

    for job, operations in jobs.items():
        total_time = 0
        for machines, times in operations:
            total_time += min(times)
        remaining_work[job] = total_time

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    import random

    while available_operations:
        # Prioritize operations based on Least Work Remaining and Random machine
        best_op = None
        best_start_time = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Randomly select a machine from available machines
            selected_machine_index = random.randint(0, len(machines) - 1)
            selected_machine = machines[selected_machine_index]
            selected_time = times[selected_machine_index]

            # Calculate start time
            start_time = max(machine_available_times[selected_machine], job_completion_times[job_id])

            if start_time < best_start_time:
                best_start_time = start_time
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

        # Update machine availability, job completion time, and remaining work
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        remaining_work[job_id] -= best_time

        # Remove scheduled operation and add the next operation (if any)
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
