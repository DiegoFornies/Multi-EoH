
def heuristic(input_data):
    """Schedules jobs considering machine load and operation slack."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_remaining_times = {}

    for job_id, operations in jobs.items():
        total_remaining_time = 0
        for op_idx in range(len(operations)):
            machines, times = operations[op_idx]
            total_remaining_time += min(times)
        job_remaining_times[job_id] = total_remaining_time

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        # Prioritize operations based on shortest processing time, earliest start time,
        # and machine load balancing.
        best_op = None
        best_start_time = float('inf')
        best_processing_time = float('inf')
        best_machine_load = float('inf')  # Lower is better

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Find the earliest possible start time for this operation
            earliest_start_time = float('-inf')
            selected_machine = None
            selected_time = None

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])

                if earliest_start_time > start_time or earliest_start_time == float('-inf'):
                    earliest_start_time = start_time
                    selected_machine = machine
                    selected_time = time

            processing_time = selected_time
            machine_load = machine_available_times[selected_machine] + processing_time

            # Prioritize based on earliest start, shortest process, and machine load.
            # Incorporate remaining job time as a tiebreaker.
            if (earliest_start_time < best_start_time or
                (earliest_start_time == best_start_time and processing_time < best_processing_time) or
                (earliest_start_time == best_start_time and processing_time == best_processing_time and machine_load < best_machine_load)):

                best_start_time = earliest_start_time
                best_processing_time = processing_time
                best_machine_load = machine_load
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

        # Update machine availability and job completion time
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        job_remaining_times[job_id] -= best_time


        # Remove the scheduled operation from available operations and add the next operation (if any)
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
