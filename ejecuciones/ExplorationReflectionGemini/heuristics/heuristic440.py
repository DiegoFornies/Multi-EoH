
def heuristic(input_data):
    """Schedules jobs using a combined SPT and load balancing approach."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        # Prioritize operations based on shortest processing time, earliest start time, and machine load
        best_op = None
        best_start_time = float('inf')
        best_processing_time = float('inf')
        best_machine_load = float('inf') # Lower load is better

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Find the earliest possible start time and machine load for this operation
            earliest_start_time = float('-inf')
            selected_machine = None
            selected_time = None
            selected_load = float('inf')

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                load = machine_load[machine] #Consider machine load in heuristic.

                if earliest_start_time > start_time or earliest_start_time == float('-inf'):
                    earliest_start_time = start_time
                    selected_machine = machine
                    selected_time = time
                    selected_load = load

                elif earliest_start_time == start_time and load < selected_load: # Tie-breaker: prefer less loaded machines
                    selected_machine = machine
                    selected_time = time
                    selected_load = load

            processing_time = selected_time

            if earliest_start_time < best_start_time or \
               (earliest_start_time == best_start_time and processing_time < best_processing_time) or \
               (earliest_start_time == best_start_time and processing_time == best_processing_time and selected_load < best_machine_load):

                best_start_time = earliest_start_time
                best_processing_time = processing_time
                best_op = op_data
                best_machine = selected_machine
                best_time = selected_time
                best_machine_load = selected_load

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

        # Update machine availability, job completion time, and machine load
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_load[best_machine] += best_time #Update machine load

        # Remove the scheduled operation from available operations and add the next operation (if any)
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
