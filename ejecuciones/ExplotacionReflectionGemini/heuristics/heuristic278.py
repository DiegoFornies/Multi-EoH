
def heuristic(input_data):
    """Combines SPT, machine load, and local search for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    remaining_operations = {j: len(jobs[j]) for j in range(1, n_jobs + 1)}

    operations = []
    for job_id in jobs:
        for op_idx, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, op_data))

    scheduled_operations = set()

    while any(remaining_operations[job] > 0 for job in range(1, n_jobs + 1)):
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
            if job_id not in jobs:
                continue
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
        min_score = float('inf')

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                end_time = start_time + time
                remaining = remaining_operations[job_id]
                machine_load_factor = machine_load[machine]
                score = start_time + remaining + machine_load_factor + time

                if score < min_score:
                    min_score = score
                    best_operation = (job_id, op_idx, op_data, machine, start_time, time)

        if best_operation:
            job_id, op_idx, op_data, machine, start_time, time = best_operation
            end_time = start_time + time
            op_num = op_idx + 1

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': time
            })

            machine_available_time[machine] = end_time
            job_last_end_time[job_id] = end_time
            machine_load[machine] += time
            remaining_operations[job_id] -= 1
            scheduled_operations.add((job_id, op_idx))

        else:
            break

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

    best_schedule = schedule
    best_objectives = objective_functions(best_schedule)

    #Improvement by swapping operations of same job to reduce balance
    for job_id in jobs:
        if len(schedule[job_id])>1:
            for i in range(len(schedule[job_id])-1):
                for j in range(i+1, len(schedule[job_id])):

                    original_schedule = {job_id: [op.copy() for op in schedule[job_id]]}
                    original_obj = objective_functions(schedule)
                    #Make a local copy of the schedule
                    temp_schedule = {job_id: [op.copy() for op in schedule[job_id]]}
                    
                    #Swap Assigned Machine
                    op1_original_machine = temp_schedule[job_id][i]['Assigned Machine']
                    op2_original_machine = temp_schedule[job_id][j]['Assigned Machine']
                    
                    temp_schedule[job_id][i]['Assigned Machine'] = op2_original_machine
                    temp_schedule[job_id][j]['Assigned Machine'] = op1_original_machine
                    
                    #Check Machine constraint
                    machines1 = jobs[job_id][i][0]
                    machines2 = jobs[job_id][j][0]
                    
                    #Check machine feasibility
                    if temp_schedule[job_id][i]['Assigned Machine'] not in machines1 or \
                        temp_schedule[job_id][j]['Assigned Machine'] not in machines2:
                        continue #Skip to next iteration
                    
                    processing_time_op1 = jobs[job_id][i][1][machines1.index(temp_schedule[job_id][i]['Assigned Machine'])]
                    processing_time_op2 = jobs[job_id][j][1][machines2.index(temp_schedule[job_id][j]['Assigned Machine'])]

                    #Update Processing Time
                    temp_schedule[job_id][i]['Processing Time'] = processing_time_op1
                    temp_schedule[job_id][j]['Processing Time'] = processing_time_op2
                    
                    # Update the start and end times based on the new machine assignments.
                    machine_available_time = {m: 0 for m in range(n_machines)}
                    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
                    
                    #Reschedule for current job
                    for op_idx_temp in range(len(temp_schedule[job_id])):
                        machine = temp_schedule[job_id][op_idx_temp]['Assigned Machine']
                        processing_time = temp_schedule[job_id][op_idx_temp]['Processing Time']
                        
                        start_time = max(machine_available_time[machine], job_completion_time[job_id])
                        end_time = start_time + processing_time
                        
                        temp_schedule[job_id][op_idx_temp]['Start Time'] = start_time
                        temp_schedule[job_id][op_idx_temp]['End Time'] = end_time
                        
                        machine_available_time[machine] = end_time
                        job_completion_time[job_id] = end_time
                    
                    #Update total schedule
                    schedule[job_id] = temp_schedule[job_id]
                    new_objectives = objective_functions(schedule)
                    
                    if new_objectives['Balance'] < original_obj['Balance']:
                        # update the start and end times based on the new assignments.
                        best_schedule = schedule
                        best_objectives = new_objectives

                        #Update other jobs
                        machine_available_time = {m: 0 for m in range(n_machines)}
                        job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
                        
                        #Full schedule recalculated
                        for job_id_re in range(1, n_jobs+1):
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
