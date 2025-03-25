
def heuristic(input_data):
    """
    Hybrid heuristic: Initial greedy makespan minimization, then balance improvement via operation swaps.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job_id: [] for job_id in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    eligible_operations = [(job_id, 0) for job_id in range(1, n_jobs + 1)]

    while eligible_operations:
        best_operation = None
        earliest_end_time = float('inf')

        for job_id, op_idx in eligible_operations:
            machines, times = jobs[job_id][op_idx]
            
            # find the machine available earliest for the operation
            best_machine, min_end_time = -1, float('inf')
            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine

            if min_end_time < earliest_end_time:
                earliest_end_time = min_end_time
                best_operation = (job_id, op_idx, best_machine, times[machines.index(best_machine)])
        
        job_id, op_idx, assigned_machine, processing_time = best_operation
        start_time = max(machine_available_time[assigned_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[assigned_machine] = end_time
        job_completion_time[job_id] = end_time
        eligible_operations.remove((job_id, op_idx))

        if op_idx + 1 < len(jobs[job_id]):
            eligible_operations.append((job_id, op_idx + 1))
            
    # Phase 2: Balance Improvement (Local Search - Swap Operations)
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
        separation = 0  # Not meaningful in this context

        return {'Makespan': makespan, 'Separation': separation, 'Balance': balance}
    
    best_schedule = schedule
    best_objectives = objective_functions(best_schedule)

    #Improvement by swapping operations of same job to reduce balance
    for job_id in range(1,n_jobs+1):
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

                    current_job_schedule = []
                    
                    #Reschedule for current job
                    for op_idx in range(len(temp_schedule[job_id])):
                        machine = temp_schedule[job_id][op_idx]['Assigned Machine']
                        processing_time = temp_schedule[job_id][op_idx]['Processing Time']
                        
                        start_time = max(machine_available_time[machine], job_completion_time[job_id])
                        end_time = start_time + processing_time
                        
                        temp_schedule[job_id][op_idx]['Start Time'] = start_time
                        temp_schedule[job_id][op_idx]['End Time'] = end_time
                        
                        machine_available_time[machine] = end_time
                        job_completion_time[job_id] = end_time
                        current_job_schedule.append(temp_schedule[job_id][op_idx])
                        
                    #Update total schedule
                    schedule[job_id] = current_job_schedule
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
