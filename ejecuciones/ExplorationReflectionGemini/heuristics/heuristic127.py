
def heuristic(input_data):
    """Schedules jobs considering shortest processing time and machine load."""
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
        best_makespan = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Calculate the makespan for each machine
            makespans = {}
            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + time
                makespans[machine] = end_time
            
            # Select machine based on minimum makespan
            best_machine = min(makespans, key=makespans.get)
            best_time = times[machines.index(best_machine)]

            if makespans[best_machine] < best_makespan:
                best_makespan = makespans[best_machine]
                best_op = op_data
                best_processing_time = best_time
                best_start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
                best_assigned_machine = best_machine

        # Schedule the best operation
        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        start_time = best_start_time
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability and job completion time
        machine_available_times[best_assigned_machine] = end_time
        job_completion_times[job_id] = end_time

        # Remove the scheduled operation from available operations and add the next operation (if any)
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
