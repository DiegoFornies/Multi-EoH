
def heuristic(input_data):
    """Schedules jobs based on earliest finish time and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    job_current_operation = {j: 1 for j in jobs_data}

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
        best_operation = None
        earliest_finish_time = float('inf')

        for operation in available_operations:
            job_id = operation['job_id']
            machines = operation['machines']
            times = operation['times']

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]

                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + time

                if end_time < earliest_finish_time:
                    earliest_finish_time = end_time
                    best_operation = (operation, machine, time, start_time)

        if best_operation is None:
            break

        operation, best_machine, processing_time, start_time = best_operation
        job_id = operation['job_id']
        op_idx = operation['op_idx']
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

        available_operations = [
            op for op in operations
            if op['op_idx'] == job_current_operation[op['job_id']]
            and not any(
                sch_op['Operation'] == op['op_idx'] and sch_op['Assigned Machine'] is not None
                for job_schedule in schedule.values()
                for sch_op in job_schedule
            )
        ]

    return schedule
