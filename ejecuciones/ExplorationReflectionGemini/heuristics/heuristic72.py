
def heuristic(input_data):
    """Schedules jobs by prioritizing shortest processing time and earliest start time."""

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
        # Prioritize operations based on shortest processing time and earliest start time
        best_op = None
        best_start_time = float('inf')
        best_processing_time = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Find the earliest possible start time for this operation
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                
                if start_time < best_start_time or (start_time == best_start_time and processing_time < best_processing_time):
                    best_start_time = start_time
                    best_processing_time = processing_time
                    best_op = op_data
                    best_machine = machine
                    best_time = processing_time
        
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

        # Remove the scheduled operation from available operations and add the next operation (if any)
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
