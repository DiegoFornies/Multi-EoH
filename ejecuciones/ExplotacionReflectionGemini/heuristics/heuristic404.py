
def heuristic(input_data):
    """Hybrid heuristic: Combines makespan minimization with balance improvement."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    remaining_operations = {j: len(jobs[j]) for j in range(1, n_jobs + 1)}
    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, op_data))

    scheduled_operations = set()

    while any(remaining_operations[job] > 0 for job in range(1, n_jobs + 1)):
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
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
        min_start_time = float('inf')

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_operation = (job_id, op_idx, machine, start_time, processing_time)

        if best_operation:
            job_id, op_idx, machine, start_time, processing_time = best_operation
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
            remaining_operations[job_id] -= 1
            scheduled_operations.add((job_id, op_idx))
        else:
            break

    # Balance Improvement - Swap operations within jobs
    def calculate_machine_load(current_schedule):
        machine_load = {m: 0 for m in range(n_machines)}
        for job_id in current_schedule:
            for operation in current_schedule[job_id]:
                machine_load[operation['Assigned Machine']] += operation['Processing Time']
        return machine_load

    def objective_functions(current_schedule):
        machine_load = calculate_machine_load(current_schedule)
        makespan = max(job_completion_time.values()) if job_completion_time else 0 #calculate makespan
        total_load = sum(machine_load.values())
        n_machines_used = len([m for m in machine_load if machine_load[m] > 0])
        if n_machines_used > 0:
            balance = sum([(machine_load[m] - (total_load / n_machines_used)) ** 2 for m in machine_load if machine_load[m] > 0]) / n_machines_used
        else:
            balance = 0
        separation = 0

        return {'Makespan': makespan, 'Separation': separation, 'Balance': balance}

    best_schedule = schedule
    best_objectives = objective_functions(best_schedule)

    # Local search
    for job_id in range(1, n_jobs + 1):
        if len(schedule[job_id]) > 1:
            for i in range(len(schedule[job_id]) - 1):
                for j in range(i + 1, len(schedule[job_id])):
                    original_schedule = {job_id: [op.copy() for op in schedule[job_id]]}
                    original_obj = objective_functions(schedule)

                    temp_schedule = {job_id: [op.copy() for op in schedule[job_id]]}

                    op1_original_machine = temp_schedule[job_id][i]['Assigned Machine']
                    op2_original_machine = temp_schedule[job_id][j]['Assigned Machine']

                    temp_schedule[job_id][i]['Assigned Machine'] = op2_original_machine
                    temp_schedule[job_id][j]['Assigned Machine'] = op1_original_machine

                    machines1 = jobs[job_id][i][0]
                    machines2 = jobs[job_id][j][0]

                    if temp_schedule[job_id][i]['Assigned Machine'] not in machines1 or \
                       temp_schedule[job_id][j]['Assigned Machine'] not in machines2:
                        continue

                    processing_time_op1 = jobs[job_id][i][1][machines1.index(temp_schedule[job_id][i]['Assigned Machine'])]
                    processing_time_op2 = jobs[job_id][j][1][machines2.index(temp_schedule[job_id][j]['Assigned Machine'])]

                    temp_schedule[job_id][i]['Processing Time'] = processing_time_op1
                    temp_schedule[job_id][j]['Processing Time'] = processing_time_op2

                    machine_available_time = {m: 0 for m in range(n_machines)}
                    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

                    current_job_schedule = []

                    for op_idx_re in range(len(temp_schedule[job_id])):
                        machine = temp_schedule[job_id][op_idx_re]['Assigned Machine']
                        processing_time = temp_schedule[job_id][op_idx_re]['Processing Time']

                        start_time = max(machine_available_time[machine], job_completion_time[job_id])
                        end_time = start_time + processing_time

                        temp_schedule[job_id][op_idx_re]['Start Time'] = start_time
                        temp_schedule[job_id][op_idx_re]['End Time'] = end_time

                        machine_available_time[machine] = end_time
                        job_completion_time[job_id] = end_time
                        current_job_schedule.append(temp_schedule[job_id][op_idx_re])

                    schedule[job_id] = current_job_schedule
                    new_objectives = objective_functions(schedule)

                    if new_objectives['Balance'] < original_obj['Balance']:
                        best_schedule = schedule
                        best_objectives = new_objectives

                        machine_available_time = {m: 0 for m in range(n_machines)}
                        job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

                        for job_id_re in range(1, n_jobs + 1):
                            for op_idx_re in range(len(schedule[job_id_re])):
                                machine = schedule[job_id_re][op_idx_re]['Assigned Machine']
                                processing_time = schedule[job_id_re][op_idx_re]['Processing Time']

                                start_time = max(machine_available_time[machine], job_completion_time[job_id_re])
                                end_time = start_time + processing_time

                                schedule[job_id_re][op_idx_re]['Start Time'] = start_time
                                schedule[job_id_re][op_idx_re]['End Time'] = end_time

                                machine_available_time[machine] = end_time
                                job_completion_time[job_id_re] = end_time
                    else:
                        schedule[job_id] = original_schedule[job_id]

    return best_schedule
