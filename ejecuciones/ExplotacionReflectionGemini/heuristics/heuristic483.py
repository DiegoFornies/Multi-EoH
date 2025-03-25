
def heuristic(input_data):
    """Hybrid heuristic: Greedy EFT + load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    scheduled_operations = set()

    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, op_data))

    while any(len(schedule[job_id]) < len(jobs[job_id]) for job_id in range(1, n_jobs + 1)):
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
            if len(schedule[job_id]) == op_idx and (job_id, op_idx) not in scheduled_operations:
                eligible_operations.append((job_id, op_idx, op_data))

        if not eligible_operations:
            break

        best_operation = None
        best_machine = None
        earliest_end_time = float('inf')

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data
            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < earliest_end_time:
                    earliest_end_time = end_time
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)

        if best_operation:
            job_id, op_idx = best_operation
            machine, processing_time = best_machine
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = end_time
            job_completion_time[job_id] = end_time
            scheduled_operations.add((job_id, op_idx))

    # Load Balancing - machine reassignment.
    machine_load = {m: 0 for m in range(n_machines)}
    for job_id in range(1, n_jobs + 1):
        for operation in schedule[job_id]:
            machine_load[operation['Assigned Machine']] += operation['Processing Time']

    total_load = sum(machine_load.values())
    n_machines_used = len([m for m in machine_load if machine_load[m] > 0])
    if n_machines_used > 0:
        average_load = total_load / n_machines_used
    else:
        average_load = 0

    for job_id in range(1, n_jobs + 1):
        for op_idx in range(len(schedule[job_id])):
            operation = schedule[job_id][op_idx]
            original_machine = operation['Assigned Machine']
            original_start_time = operation['Start Time']
            original_end_time = operation['End Time']
            original_processing_time = operation['Processing Time']
            machines = jobs[job_id][op_idx][0]

            if len(machines) > 1:
                best_new_machine = original_machine
                best_start_time = original_start_time
                best_end_time = original_end_time
                best_processing_time = original_processing_time
                min_load_difference = float('inf')

                for new_machine_idx, new_machine in enumerate(machines):
                    if new_machine != original_machine:
                        new_processing_time = jobs[job_id][op_idx][1][new_machine_idx]
                        start_time = max(machine_available_time[new_machine], job_completion_time[job_id])
                        end_time = start_time + new_processing_time

                        load_difference = abs((machine_load[new_machine] - average_load) - (machine_load[original_machine] - average_load))
                        if load_difference < min_load_difference:
                            min_load_difference = load_difference
                            best_new_machine = new_machine
                            best_start_time = start_time
                            best_end_time = end_time
                            best_processing_time = new_processing_time

                if best_new_machine != original_machine:
                    machine_load[original_machine] -= original_processing_time
                    machine_load[best_new_machine] += best_processing_time

                    schedule[job_id][op_idx]['Assigned Machine'] = best_new_machine
                    schedule[job_id][op_idx]['Start Time'] = best_start_time
                    schedule[job_id][op_idx]['End Time'] = best_end_time
                    schedule[job_id][op_idx]['Processing Time'] = best_processing_time

                    machine_available_time[original_machine] = original_start_time #Free up previously assigned machine
                    machine_available_time[best_new_machine] = best_end_time #Update the schedule for assigned machine
                    job_completion_time[job_id] = max([operation['End Time'] for operation in schedule[job_id]]) if schedule[job_id] else 0
                    #recalculate machine_available_time
                    machine_available_time = {m: 0 for m in range(n_machines)}
                    for job_id_2 in range(1, n_jobs + 1):
                        for operation_2 in schedule[job_id_2]:
                            machine_available_time[operation_2['Assigned Machine']] = max(machine_available_time[operation_2['Assigned Machine']], operation_2['End Time'])


    return schedule
