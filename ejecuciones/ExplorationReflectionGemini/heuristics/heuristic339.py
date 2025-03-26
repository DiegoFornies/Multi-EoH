
def heuristic(input_data):
    """Schedules jobs considering machine load and operation urgency."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)} # Keep track of machine load
    schedule = {j: [] for j in jobs}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        # Prioritize operations based on urgency (remaining processing time),
        # shortest processing time, machine load, and earliest start time
        best_op = None
        best_start_time = float('inf')
        best_urgency = float('inf')
        best_load = float('inf')
        best_processing_time = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Find the earliest possible start time for this operation
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

            # Calculate job urgency (remaining processing time of the job)
            remaining_time = 0
            for i in range(op_idx, len(jobs[job_id])):
                remaining_time += min(jobs[job_id][i][1])

            # Prioritize operations based on urgency, start time, and machine load.
            current_load = machine_load[selected_machine]

            if (remaining_time < best_urgency) or \
               (remaining_time == best_urgency and earliest_start_time < best_start_time) or \
               (remaining_time == best_urgency and earliest_start_time == best_start_time and processing_time < best_processing_time) or \
               (remaining_time == best_urgency and earliest_start_time == best_start_time and processing_time == best_processing_time and current_load < best_load):

                best_start_time = earliest_start_time
                best_urgency = remaining_time
                best_op = op_data
                best_machine = selected_machine
                best_time = selected_time
                best_load = current_load

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

        # Update machine availability, job completion time and machine load
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_load[best_machine] += best_time

        # Remove the scheduled operation from available operations and add the next operation (if any)
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
