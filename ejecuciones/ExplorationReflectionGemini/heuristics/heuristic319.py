
def heuristic(input_data):
    """Schedules jobs with dynamic priority based on remaining work and machine load."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_remaining_times = {}
    for job_id, operations in jobs.items():
        job_remaining_times[job_id] = sum(min(times) for machines, times in operations) #Estimate remaining processing time

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        # Prioritize operations based on remaining work and machine load
        best_op = None
        best_score = float('inf')


        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Find the best machine for this operation
            best_machine = None
            best_time = float('inf')
            earliest_start_time = float('inf')

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                if start_time < earliest_start_time:
                  earliest_start_time = start_time
                  best_machine = machine
                  best_time = time


            #Calculate a score considering remaining time of job and machine load
            machine_load = machine_available_times[best_machine]
            remaining_time = job_remaining_times[job_id]
            score = earliest_start_time + best_time + 0.5*machine_load - 0.2*remaining_time #Adjustable weights
            #score = earliest_start_time + best_time + machine_load

            if score < best_score:
                best_score = score
                best_op = op_data
                selected_machine = best_machine
                selected_time = best_time
                start_time = earliest_start_time


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

        # Update machine availability, job completion time and remaining time
        machine_available_times[selected_machine] = end_time
        job_completion_times[job_id] = end_time
        job_remaining_times[job_id] -= selected_time



        # Remove the scheduled operation from available operations and add the next operation (if any)
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
