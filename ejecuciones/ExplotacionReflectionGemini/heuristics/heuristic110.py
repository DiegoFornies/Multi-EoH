
def heuristic(input_data):
    """Combines job priority and machine utilization for FJSSP scheduling."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in jobs_data}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data}
    remaining_operations = {job: 0 for job in jobs_data}

    for job in jobs_data:
        remaining_operations[job] = len(jobs_data[job])
    
    operations = []
    for job_id in jobs_data:
        for op_idx, op_data in enumerate(jobs_data[job_id]):
            operations.append((job_id, op_idx, op_data))

    scheduled_operations = set()

    while any(remaining_operations[job] > 0 for job in jobs_data):
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
            if remaining_operations[job_id] > 0 and (job_id, op_idx) not in scheduled_operations:
                is_next_operation = True
                if op_idx > 0:
                    if (job_id, op_idx - 1) not in scheduled_operations:
                        is_next_operation = False

                if is_next_operation:
                    eligible_operations.append((job_id, op_idx, op_data))

        if not eligible_operations:
            break

        best_operation = None
        min_remaining = float('inf')
        min_makespan = float('inf')
        min_machine_load = float('inf')

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data
            remaining = remaining_operations[job_id]
            
            best_machine = -1
            best_time = float('inf')
            best_start_time = 0
            best_processing_time = 0
            
            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]

                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + time

                if end_time < best_time:
                    best_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = time

            if remaining < min_remaining:
                min_remaining = remaining
                min_makespan = best_time
                best_operation = (job_id, op_idx, op_data, best_machine, best_start_time, best_processing_time)

            elif remaining == min_remaining and best_time < min_makespan:
                min_makespan = best_time
                best_operation = (job_id, op_idx, op_data, best_machine, best_start_time, best_processing_time)

            #Tie breaker: Balance the machine load:
            elif remaining == min_remaining and best_time == min_makespan:
                machine = best_machine
                if machine_available_time[machine] < min_machine_load:
                  min_machine_load = machine_available_time[machine]
                  best_operation = (job_id, op_idx, op_data, best_machine, best_start_time, best_processing_time)
        

        job_id, op_idx, op_data, machine, start_time, processing_time = best_operation
        op_num = op_idx + 1
        schedule[job_id].append({'Operation': op_num, 'Assigned Machine': machine, 'Start Time': start_time, 'End Time': start_time + processing_time, 'Processing Time': processing_time})
        
        machine_available_time[machine] = start_time + processing_time
        job_completion_time[job_id] = start_time + processing_time
        remaining_operations[job_id] -= 1
        scheduled_operations.add((job_id, op_idx))

    return schedule
