
def heuristic(input_data):
    """
    Adaptive heuristic balances SPT, load, separation, and remaining ops.
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
        # Adaptive Weighting (Example - can be further refined)
        makespan_urgency = 0.4
        load_balance_urgency = 0.3
        separation_urgency = 0.1
        remaining_ops_urgency = 0.2

        # Calculate Machine Load
        machine_load = {m: machine_available_time[m] for m in range(n_machines)}
        avg_machine_load = sum(machine_load.values()) / n_machines if n_machines > 0 else 0

        def calculate_priority(operation):
            job_id = operation['job_id']
            machines = operation['machines']
            times = operation['times']

            best_machine = None
            min_weighted_time = float('inf')
            processing_time = None

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]

                available_time = machine_available_time[machine]
                start_time = max(available_time, job_completion_time[job_id])
                end_time = start_time + time

                # SPT Component
                spt_score = time

                # Load Balancing Component
                load_score = max(0, machine_load[machine] - avg_machine_load) #Penalty for adding to loaded machines

                # Separation Component (Simple - can be improved)
                separation_score = available_time - job_completion_time[job_id] if available_time > job_completion_time[job_id] else 0

                # Remaining Ops Component
                remaining_ops = job_remaining_operations[job_id]
                remaining_ops_score = remaining_ops #Prioritize jobs with fewer operations remaining

                weighted_time = (
                    makespan_urgency * spt_score +
                    load_balance_urgency * load_score - #minimize makespan load
                    separation_urgency * separation_score - #maximize separation
                    remaining_ops_urgency * remaining_ops_score
                )

                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_machine = machine
                    processing_time = time

            return min_weighted_time, best_machine, processing_time

        # Sort available operations by dynamically calculated priority
        prioritized_operations = []
        for op in available_operations:
             priority, machine, time = calculate_priority(op)
             prioritized_operations.append((op, priority, machine, time))

        prioritized_operations.sort(key=lambda x: x[1]) # Sort by priority

        operation, _, best_machine, processing_time = prioritized_operations[0]

        job_id = operation['job_id']
        op_idx = operation['op_idx']

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
        job_current_operation[job_id] += 1
        job_remaining_operations[job_id] -= 1
        available_operations = [op for op in operations if op['op_idx'] == job_current_operation[op['job_id']]]
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
