
def heuristic(input_data):
    """
    Schedules jobs by prioritizing operations with the shortest processing time
    and assigning them to the least loaded machine among feasible options.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines + 1)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    available_operations = []
    for job_id, operations in jobs_data.items():
        available_operations.append((job_id, 0))  # (job_id, operation_index)

    scheduled_operations = set()

    while available_operations:
        best_operation = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs_data[job_id][op_idx]

            # Find the machine with the earliest available time among feasible machines
            best_local_machine = None
            min_local_end_time = float('inf')
            
            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]

                available_time_on_machine = machine_load[machine]
                start_time = max(job_completion_times[job_id], available_time_on_machine)
                end_time = start_time + processing_time
                
                if end_time < min_local_end_time:
                    min_local_end_time = end_time
                    best_local_machine = (machine, start_time, processing_time)

            if best_local_machine is not None and min_local_end_time < min_end_time:
                min_end_time = min_local_end_time
                best_operation = (job_id, op_idx)
                best_machine = best_local_machine
        
        if best_operation is None:
            break

        job_id, op_idx = best_operation
        machine, start_time, processing_time = best_machine

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': start_time + processing_time,
            'Processing Time': processing_time
        })

        machine_load[machine] = start_time + processing_time
        job_completion_times[job_id] = start_time + processing_time

        available_operations.remove((job_id, op_idx))
        scheduled_operations.add((job_id, op_idx))

        # Add the next operation of the same job, if any
        if op_idx + 1 < len(jobs_data[job_id]):
            available_operations.append((job_id, op_idx + 1))

    return schedule
