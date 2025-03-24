
def heuristic(input_data):
    """Combines SPT, machine idle time, and dynamic load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    machine_load = {m: 0 for m in range(n_machines)}

    operations = []
    for job_id, job in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx + 1,
                'machines': machines,
                'times': times
            })

    while operations:
        eligible_operations = []
        for op in operations:
            job_id = op['job_id']
            op_idx = op['op_idx']
            
            is_eligible = True
            # Check if all preceding operations of the job are scheduled
            for scheduled_op in schedule[job_id]:
                if scheduled_op['Operation'] >= op_idx:
                    is_eligible = False
                    break
            if op_idx > 1:
                preceding_op_found = False
                for scheduled_op in schedule[job_id]:
                    if scheduled_op['Operation'] == op_idx - 1:
                        preceding_op_found = True
                        break
                if not preceding_op_found and op_idx !=1 :
                    is_eligible = False
                    
            if is_eligible:
                is_operation_scheduled = False
                for scheduled_job in schedule.values():
                    for scheduled_operation in scheduled_job:
                        if scheduled_operation['Operation'] == op_idx and scheduled_operation:
                            is_operation_scheduled = True
                            break
                    if is_operation_scheduled:
                        break
                if not is_operation_scheduled:
                     eligible_operations.append(op)

        if not eligible_operations:
            break

        # Dynamically adjust weights based on machine load
        load_weights = {m: 1 + (machine_load[m] / sum(machine_load.values()) if sum(machine_load.values()) > 0 else 0) for m in range(n_machines)}

        best_operation = None
        best_machine = None
        min_weighted_end_time = float('inf')
        processing_time = 0
        
        for operation in eligible_operations:
            job_id = operation['job_id']
            machines = operation['machines']
            times = operation['times']

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]

                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + time
                weighted_end_time = end_time * load_weights[machine]
                
                if weighted_end_time < min_weighted_end_time:
                    min_weighted_end_time = weighted_end_time
                    best_operation = operation
                    best_machine = machine
                    processing_time = time

        if best_operation is None:
            break

        job_id = best_operation['job_id']
        op_idx = best_operation['op_idx']

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time
        
        schedule[job_id].append({
            'Operation': op_idx,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        machine_load[best_machine] += processing_time
        
        operations.remove(best_operation)
    return schedule
