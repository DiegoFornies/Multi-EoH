
def heuristic(input_data):
    """Schedules jobs using SPT and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, 1 + n_jobs)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, 1 + n_jobs)}
    machine_load = {m: 0 for m in range(n_machines)}

    remaining_operations = {j: len(jobs_data[j]) for j in range(1, 1 + n_jobs)}
    scheduled_operations = set()
    
    operations = []
    for job_id in jobs_data:
        for op_idx, op_data in enumerate(jobs_data[job_id]):
            operations.append((job_id, op_idx, op_data))

    while any(remaining_operations[job] > 0 for job in range(1, 1 + n_jobs)):
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
            if job_id not in jobs_data:
                continue
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
        min_weighted_time = float('inf')

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data
            best_machine = -1
            best_start_time = float('inf')
            best_processing_time = float('inf')
            
            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                end_time = start_time + time
                weighted_time = end_time + machine_load[machine]
                
                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = time
                elif weighted_time == min_weighted_time:
                    if machine_load[machine] < machine_load[best_machine]:
                        best_machine = machine
                        best_start_time = start_time
                        best_processing_time = time
            
            if best_machine != -1:
                best_operation = (job_id, op_idx, best_machine, best_start_time, best_processing_time)
                #break # Removing early stop to check all operations

        if best_operation:
            job_id, op_idx, best_machine, best_start_time, best_processing_time = best_operation
            op_num = op_idx + 1
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })
            
            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_last_end_time[job_id] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            remaining_operations[job_id] -= 1
            scheduled_operations.add((job_id, op_idx))
    return schedule
