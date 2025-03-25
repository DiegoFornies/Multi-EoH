
def heuristic(input_data):
    """Combines greedy makespan, local search (swap/reassign) for balance, and insertion."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    while available_operations:
        best_operation = None
        best_machine = None
        earliest_end_time = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < earliest_end_time:
                    earliest_end_time = end_time
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)

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
        available_operations.remove((job_id, op_idx))

        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))

    def calculate_machine_load(current_schedule):
        machine_load = {m: 0 for m in range(n_machines)}
        for job_id in current_schedule:
            for operation in current_schedule[job_id]:
                machine_load[operation['Assigned Machine']] += operation['Processing Time']
        return machine_load

    def calculate_makespan(current_schedule):
        makespan = 0
        for job_id in current_schedule:
            if schedule[job_id]:
                makespan = max(makespan, schedule[job_id][-1]['End Time'])
        return makespan

    def objective_functions(current_schedule):
        machine_load = calculate_machine_load(current_schedule)
        makespan = calculate_makespan(current_schedule)
        total_load = sum(machine_load.values())
        n_machines_used = len([m for m in machine_load if machine_load[m] > 0])
        if n_machines_used > 0:
            balance = sum([(machine_load[m] - (total_load / n_machines_used)) ** 2 for m in machine_load if machine_load[m] > 0]) / n_machines_used
        else:
            balance = 0
        separation = 0

        return {'Makespan': makespan, 'Separation': separation, 'Balance': balance}

    best_schedule = {k: [op.copy() for op in v] for k, v in schedule.items()}
    best_objectives = objective_functions(best_schedule)

    # Local search: Swap, reassign, and insertion. Focus on balance.
    for job_id in range(1, n_jobs + 1):
        # Swap within a job
        if len(schedule[job_id]) > 1:
            for i in range(len(schedule[job_id]) - 1):
                for j in range(i + 1, len(schedule[job_id])):
                    original_schedule = {k: [op.copy() for op in v] for k, v in schedule.items()}
                    original_obj = objective_functions(original_schedule)

                    temp_schedule = {k: [op.copy() for op in v] for k, v in schedule.items()}

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

                    # Recalculate start and end times for all jobs
                    temp_machine_available_time = {m: 0 for m in range(n_machines)}
                    temp_job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

                    new_schedule = {}
                    for job_id_re in range(1, n_jobs + 1):
                        new_schedule[job_id_re] = []
                        for op_idx_re in range(len(jobs[job_id_re])):
                            machine = temp_schedule[job_id_re][op_idx_re]['Assigned Machine']
                            processing_time = temp_schedule[job_id_re][op_idx_re]['Processing Time']

                            start_time = max(temp_machine_available_time[machine], temp_job_completion_time[job_id_re])
                            end_time = start_time + processing_time

                            new_schedule[job_id_re].append({
                                'Operation': op_idx_re + 1,
                                'Assigned Machine': machine,
                                'Start Time': start_time,
                                'End Time': end_time,
                                'Processing Time': processing_time
                            })
                            temp_machine_available_time[machine] = end_time
                            temp_job_completion_time[job_id_re] = end_time

                    new_objectives = objective_functions(new_schedule)

                    if new_objectives['Balance'] < best_objectives['Balance']:
                        best_schedule = {k: [op.copy() for op in v] for k, v in new_schedule.items()}
                        best_objectives = new_objectives
                        schedule = {k: [op.copy() for op in v] for k, v in new_schedule.items()}
                    else:
                        schedule = {k: [op.copy() for op in v] for k, v in original_schedule.items()}

        # Reassignment of the machine
        for op_idx in range(len(schedule[job_id])):
            original_schedule = {k: [op.copy() for op in v] for k, v in schedule.items()}
            original_obj = objective_functions(original_schedule)
            original_machine = schedule[job_id][op_idx]['Assigned Machine']

            machines = jobs[job_id][op_idx][0]

            for new_machine in machines:
                if new_machine != original_machine:
                    temp_schedule = {k: [op.copy() for op in v] for k, v in schedule.items()}
                    temp_schedule[job_id][op_idx]['Assigned Machine'] = new_machine

                    processing_time = jobs[job_id][op_idx][1][machines.index(new_machine)]
                    temp_schedule[job_id][op_idx]['Processing Time'] = processing_time

                    # Recalculate start and end times for all jobs
                    temp_machine_available_time = {m: 0 for m in range(n_machines)}
                    temp_job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
                    new_schedule = {}

                    for job_id_re in range(1, n_jobs + 1):
                        new_schedule[job_id_re] = []
                        for op_idx_re in range(len(jobs[job_id_re])):
                            machine = temp_schedule[job_id_re][op_idx_re]['Assigned Machine']
                            processing_time = temp_schedule[job_id_re][op_idx_re]['Processing Time']

                            start_time = max(temp_machine_available_time[machine], temp_job_completion_time[job_id_re])
                            end_time = start_time + processing_time

                            new_schedule[job_id_re].append({
                                'Operation': op_idx_re + 1,
                                'Assigned Machine': machine,
                                'Start Time': start_time,
                                'End Time': end_time,
                                'Processing Time': processing_time
                            })
                            temp_machine_available_time[machine] = end_time
                            temp_job_completion_time[job_id_re] = end_time

                    new_objectives = objective_functions(new_schedule)

                    if new_objectives['Balance'] < best_objectives['Balance']:
                        best_schedule = {k: [op.copy() for op in v] for k, v in new_schedule.items()}
                        best_objectives = new_objectives
                        schedule = {k: [op.copy() for op in v] for k, v in new_schedule.items()}
                    else:
                        schedule = {k: [op.copy() for op in v] for k, v in original_schedule.items()}

        # Insertion heuristic
        for other_job_id in range(1, n_jobs + 1):
            if other_job_id != job_id:
                for op_idx in range(len(schedule[job_id])):
                    original_schedule = {k: [op.copy() for op in v] for k, v in schedule.items()}
                    original_obj = objective_functions(original_schedule)
                    
                    op_to_insert = schedule[job_id][op_idx]

                    temp_schedule = {k: [op.copy() for op in v] for k, v in schedule.items()}
                    del temp_schedule[job_id][op_idx]
                    
                    best_insert_idx = -1
                    best_temp_schedule = None
                    best_new_objectives = None
                    
                    for insert_idx in range(len(temp_schedule[other_job_id])+1):
                        temp_schedule_insert = {k: [op.copy() for op in v] for k, v in temp_schedule.items()}
                        temp_schedule_insert[other_job_id].insert(insert_idx, op_to_insert)
                        
                        temp_machine_available_time = {m: 0 for m in range(n_machines)}
                        temp_job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

                        new_schedule_insert = {}

                        for job_id_re in range(1, n_jobs + 1):
                            new_schedule_insert[job_id_re] = []
                            for op_idx_re in range(len(temp_schedule_insert[job_id_re])):
                                machine = temp_schedule_insert[job_id_re][op_idx_re]['Assigned Machine']
                                processing_time = temp_schedule_insert[job_id_re][op_idx_re]['Processing Time']

                                start_time = max(temp_machine_available_time[machine], temp_job_completion_time[job_id_re])
                                end_time = start_time + processing_time

                                new_schedule_insert[job_id_re].append({
                                    'Operation': temp_schedule_insert[job_id_re][op_idx_re]['Operation'],
                                    'Assigned Machine': machine,
                                    'Start Time': start_time,
                                    'End Time': end_time,
                                    'Processing Time': processing_time
                                })
                                temp_machine_available_time[machine] = end_time
                                temp_job_completion_time[job_id_re] = end_time

                        new_objectives_insert = objective_functions(new_schedule_insert)
                        if best_insert_idx == -1 or new_objectives_insert['Balance'] < best_new_objectives['Balance']:
                            best_insert_idx = insert_idx
                            best_temp_schedule = {k: [op.copy() for op in v] for k, v in temp_schedule_insert.items()}
                            best_new_objectives = new_objectives_insert
                    
                    if best_insert_idx != -1 and best_new_objectives['Balance'] < best_objectives['Balance']:
                        best_schedule = {k: [op.copy() for op in v] for k, v in best_temp_schedule.items()}
                        best_objectives = best_new_objectives
                        schedule = {k: [op.copy() for op in v] for k, v in best_temp_schedule.items()}

    return best_schedule
