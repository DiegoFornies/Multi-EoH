
def heuristic(input_data):
    """
    A heuristic to solve the FJSSP: Earliest Due Date (EDD) variant, balances machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    job_current_operation = {j: 1 for j in jobs_data}
    job_due_date = {}  # Calculate the due date for each job

    # Calculate due dates based on total processing time
    for job_id, job in jobs_data.items():
        total_processing_time = 0
        for machines, times in job:
            total_processing_time += min(times)  # Use shortest processing time
        job_due_date[job_id] = total_processing_time * 2 # set due date twice the processing time

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
        # Prioritize operations based on EDD and machine load
        def operation_priority(op):
            due_date = job_due_date[op['job_id']]
            min_time = min(op['times'])
            machine_loads = [machine_available_time[m] for m in op['machines']]
            avg_machine_load = sum(machine_loads) / len(machine_loads) if machine_loads else 0

            # Combine EDD and machine load
            return due_date + 0.1 * avg_machine_load  + 0.01*min_time

        available_operations.sort(key=operation_priority)

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
