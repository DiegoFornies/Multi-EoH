
def heuristic(input_data):
    """
    FJSSP heuristic: SPT, earliest machine, load balancing, remaining ops.
    Dynamically adjusts weights for optimization.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    job_current_operation = {j: 1 for j in jobs_data}
    job_remaining_operations = {j: len(jobs_data[j]) for j in jobs_data}

    operations = []
    for job_id, job in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx + 1,
                'machines': machines,
                'times': times
            })

    available_operations = [op for op in operations if op['op_idx'] == job_current_operation[op['job_id']]]

    while available_operations:
        # Dynamically adjust weights
        spt_weight = 0.4
        load_balance_weight = 0.3
        remaining_ops_weight = 0.3

        def calculate_priority(op):
            job_id = op['job_id']
            machines = op['machines']
            times = op['times']

            best_machine = None
            min_end_time = float('inf')
            processing_time = None
            machine_load = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                available_time = machine_available_time[machine]
                start_time = max(available_time, job_completion_time[job_id])
                end_time = start_time + time
                
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    processing_time = time
                    machine_load = machine_available_time[machine]

            spt_priority = processing_time if processing_time else float('inf')
            load_balance_priority = machine_load if best_machine is not None else float('inf')
            remaining_ops_priority = job_remaining_operations[job_id]

            priority = (spt_weight * spt_priority +
                        load_balance_weight * load_balance_priority +
                        remaining_ops_weight * (n_jobs - remaining_ops_priority))  #invert it so that remaining operations near the end of the jobs is given priority
            return priority

        available_operations.sort(key=calculate_priority)

        operation = available_operations.pop(0)

        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        best_machine = None
        min_end_time = float('inf')
        processing_time = None

        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]

            available_time = machine_available_time[machine]
            start_time = max(available_time, job_completion_time[job_id])
            end_time = start_time + time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = time

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
        job_remaining_operations[job_id] -= 1
        job_current_operation[job_id] += 1

        new_available_operations = []
        for op in operations:
            if op['op_idx'] == job_current_operation[op['job_id']]:
                is_scheduled = False
                for job_schedule in schedule.values():
                    for scheduled_op in job_schedule:
                        if scheduled_op['Operation'] == op['op_idx'] and scheduled_op['Assigned Machine']:
                            is_scheduled = True
                            break
                    if is_scheduled:
                        break
                if not is_scheduled:
                    new_available_operations.append(op)
        available_operations = new_available_operations

    return schedule
