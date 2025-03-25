
def heuristic(input_data):
    """
    Combines SPT and least loaded machine selection with local search
    to minimize makespan and balance machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, op_data))

    scheduled_operations = set()

    while len(scheduled_operations) < sum(len(ops) for ops in jobs.values()):
        best_operation = None
        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        for job_id, op_idx, op_data in operations:
            if (job_id, op_idx) in scheduled_operations:
                continue

            preceding_operations_scheduled = all(
                (job_id, prev_op_idx) in scheduled_operations for prev_op_idx in range(op_idx)
            )
            if not preceding_operations_scheduled:
                continue

            machines, times = op_data
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
                    best_operation = (job_id, op_idx, op_data)

        if best_operation:
            job_id, op_idx, op_data = best_operation
            operation_number = op_idx + 1
            end_time = best_start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            scheduled_operations.add((job_id, op_idx))

    # Local Search for balance (operation swap)
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
    
    best_schedule = {job_id: [op.copy() for op in schedule[job_id]] for job_id in schedule}
    best_objectives = objective_functions(best_schedule)

    for job_id in range(1,n_jobs+1):
        if len(schedule[job_id])>1:
            for i in range(len(schedule[job_id])-1):
                for j in range(i+1, len(schedule[job_id])):

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
                        
                    schedule[job_id] = current_job_schedule
                    new_objectives = objective_functions(schedule)
                    
                    if new_objectives['Balance'] < original_obj['Balance']:

                        best_schedule = {job_id_all: [op.copy() for op in schedule[job_id_all]] for job_id_all in schedule}
                        best_objectives = new_objectives
                        
                        machine_available_time = {m: 0 for m in range(n_machines)}
                        job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
                        
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
