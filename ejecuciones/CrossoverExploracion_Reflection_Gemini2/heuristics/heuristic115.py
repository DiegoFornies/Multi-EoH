
def heuristic(input_data):
    """Schedules jobs using a modified Shortest Processing Time heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    operations = []

    for job_id, job in jobs_data.items():
        for op_idx, operation in enumerate(job):
            machines, times = operation
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx + 1,
                'machines': machines,
                'times': times
            })
    while operations:
        # Find the operation with the shortest processing time among available operations
        eligible_operations = []
        for operation in operations:
            job_id = operation['job_id']
            op_idx = operation['op_idx']
            if len(schedule[job_id]) == 0:
                scheduled_ops = 0
            else:
                scheduled_ops = schedule[job_id][-1]['Operation']
            if op_idx == 1: # first operation of job
                if len(schedule[job_id]) == 0:
                  eligible_operations.append(operation)
            else:
                if op_idx - 1 == scheduled_ops:
                    eligible_operations.append(operation)

        if not eligible_operations:
          break
        
        best_operation = None
        min_end_time = float('inf')
        best_machine = None
        processing_time = None

        for operation in eligible_operations:
            job_id = operation['job_id']
            op_idx = operation['op_idx']
            machines = operation['machines']
            times = operation['times']

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_operation = operation
                    best_machine = machine
                    processing_time = time

        if best_operation is None:
            break  # No feasible operation found

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

        operations.remove(best_operation)

    return schedule
