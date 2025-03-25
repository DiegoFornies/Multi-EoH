
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP).
    Prioritizes operations with the shortest processing time available
    and selects the machine with the earliest available time.
    """
    schedule, machine_time = {}, {m: 0 for m in range(input_data['n_machines'])}
    job_last_end_time = {job: 0 for job in input_data['jobs']}
    
    eligible_operations = []
    for job, ops in input_data['jobs'].items():
        eligible_operations.append((job, 0))  # (job_id, op_index)

    scheduled_ops = set() # Keep track of scheduled operations

    while eligible_operations:
        best_op, best_machine, best_start, best_duration = None, None, float('inf'), float('inf')
        
        for job_id, op_index in eligible_operations:
            if (job_id, op_index) in scheduled_ops:
                continue

            machines, times = input_data['jobs'][job_id][op_index]

            for i in range(len(machines)):
                machine = machines[i]
                duration = times[i]
                
                start_time = max(machine_time[machine], job_last_end_time[job_id])
                
                if start_time < best_start or (start_time == best_start and duration < best_duration):
                    best_op = (job_id, op_index)
                    best_machine = machine
                    best_start = start_time
                    best_duration = duration
        
        job_id, op_index = best_op
        machine = best_machine
        duration = best_duration

        end_time = best_start + duration
        
        if job_id not in schedule:
            schedule[job_id] = []
        
        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': machine,
            'Start Time': best_start,
            'End Time': end_time,
            'Processing Time': duration
        })
        
        machine_time[machine] = end_time
        job_last_end_time[job_id] = end_time
        scheduled_ops.add((job_id, op_index))

        # Add next operation to eligible_operations if it exists
        next_op_index = op_index + 1
        if next_op_index < len(input_data['jobs'][job_id]):
            eligible_operations.append((job_id, next_op_index))
        
        eligible_operations = [op for op in eligible_operations if op not in scheduled_ops]
        eligible_operations = list(set(eligible_operations))

    return schedule
