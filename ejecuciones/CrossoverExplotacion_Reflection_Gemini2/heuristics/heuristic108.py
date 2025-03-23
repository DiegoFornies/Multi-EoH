
def heuristic(input_data):
    """
    Combines earliest avail time & min workload, prioritizes schedulable ops.
    Schedules operations ready to be processed using a combined score.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {j: 0 for j in range(1, n_jobs + 1)}

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job': job_id,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times
            })

    while operations:
        eligible_operations = []
        for operation in operations:
            if operation['operation'] == scheduled_operations[operation['job']] + 1:
                eligible_operations.append(operation)

        if eligible_operations:
            best_operation = None
            best_machine = None
            min_combined_score = float('inf')

            for operation in eligible_operations:
                job_id = operation['job']
                op_num = operation['operation']
                machines = operation['machines']
                times = operation['times']

                for i, machine in enumerate(machines):
                    processing_time = times[i]
                    start_time = max(machine_available_time[machine], job_completion_time[job_id])
                    end_time = start_time + processing_time

                    # Combine workload & availability, trying different weight
                    combined_score = 0.7 * machine_load[machine] + 0.3 * end_time

                    if combined_score < min_combined_score:
                        min_combined_score = combined_score
                        best_machine = machine
                        best_operation = operation
                        best_processing_time = processing_time
                        best_start_time = start_time

            job_id = best_operation['job']
            op_num = best_operation['operation']

            if job_id not in schedule:
                schedule[job_id] = []

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_load[best_machine] = best_start_time + best_processing_time
            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job_id] = best_start_time + best_processing_time
            scheduled_operations[job_id] = op_num

            operations.remove(best_operation)
        else:
            # If no operation is ready, select an operation with the minimum processing time
            shortest_operation = min(operations, key=lambda op: min(op['times']))
            job_id = shortest_operation['job']
            op_num = shortest_operation['operation']
            machines = shortest_operation['machines']
            times = shortest_operation['times']

            best_machine = None
            min_end_time = float('inf')
            processing_time = 0

            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    processing_time = times[i]

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            if job_id not in schedule:
                schedule[job_id] = []

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_load[best_machine] = end_time
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            scheduled_operations[job_id] = op_num

            operations.remove(shortest_operation)

    return schedule
