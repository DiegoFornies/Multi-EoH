
def heuristic(input_data):
    """Adaptive heuristic for FJSSP: dynamically prioritizes operations based on processing time, machine load, and job criticality."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_remaining_ops = {j: len(jobs[j]) for j in jobs}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        # Dynamically prioritize operations
        best_op = None
        best_priority = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Calculate the earliest possible start time and best machine
            earliest_start_time = float('inf')
            selected_machine = None
            selected_time = None

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    selected_machine = machine
                    selected_time = time

            processing_time = selected_time

            # Calculate a priority score based on:
            # 1. Shortest Processing Time (SPT)
            # 2. Machine Load (ML): Prefer less loaded machines
            # 3. Job Criticality (JC): Jobs with fewer remaining operations are prioritized

            machine_load = machine_available_times[selected_machine]  # Smaller is better
            job_criticality = job_remaining_ops[job_id]   # Smaller is better

            priority = processing_time + 0.5 * machine_load + 0.8 * job_criticality  # Tunable weights

            if priority < best_priority:
                best_priority = priority
                best_op = op_data
                best_machine = selected_machine
                best_time = selected_time
                best_start_time = earliest_start_time

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

        # Update machine availability, job completion time, and remaining operations
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        job_remaining_ops[job_id] -= 1

        # Remove the scheduled operation and add the next operation (if any)
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
