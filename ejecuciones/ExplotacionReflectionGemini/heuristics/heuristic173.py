
def heuristic(input_data):
    """Hybrid heuristic: SPT-based scheduling with balance improvement."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    while available_operations:
        best_op = None
        min_end_time = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_time[job_id])
                end_time = start_time + times[m_idx]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_op = (job_id, op_idx, m, times[m_idx])

        job_id, op_idx, assigned_machine, processing_time = best_op

        start_time = max(machine_available_times[assigned_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_times[assigned_machine] = end_time
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

    best_schedule = schedule
    best_objectives = objective_functions(best_schedule)

    # Local search to improve balance by reassigning machines for operations
    for job_id in range(1, n_jobs + 1):
        if len(schedule[job_id]) > 1:
            for i in range(len(schedule[job_id])):
                original_schedule = {job_id: [op.copy() for op in schedule[job_id]]}
                original_obj = objective_functions(schedule)
                operation = schedule[job_id][i]
                op_idx = operation['Operation'] - 1
                original_machine = operation['Assigned Machine']
                machines, times = jobs[job_id][op_idx]

                for m_idx, m in enumerate(machines):
                    if m != original_machine:
                        temp_schedule = {job_id: [op.copy() for op in schedule[job_id]]}
                        
                        #Swap machines
                        temp_schedule[job_id][i]['Assigned Machine'] = m
                        temp_schedule[job_id][i]['Processing Time'] = times[m_idx]
                        
                        #Recalculate start and end times
                        machine_available_time = {k: 0 for k in range(n_machines)}
                        job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
                        current_job_schedule = []
                    
                        for op_index in range(len(temp_schedule[job_id])):
                            machine = temp_schedule[job_id][op_index]['Assigned Machine']
                            processing_time = temp_schedule[job_id][op_index]['Processing Time']
                            
                            start_time = max(machine_available_time[machine], job_completion_time[job_id])
                            end_time = start_time + processing_time
                            
                            temp_schedule[job_id][op_index]['Start Time'] = start_time
                            temp_schedule[job_id][op_index]['End Time'] = end_time
                            
                            machine_available_time[machine] = end_time
                            job_completion_time[job_id] = end_time
                            current_job_schedule.append(temp_schedule[job_id][op_index])
                            
                        #Update Total Schedule
                        schedule[job_id] = current_job_schedule

                        new_objectives = objective_functions(schedule)

                        if new_objectives['Balance'] < original_obj['Balance']:
                            best_schedule = schedule
                            best_objectives = new_objectives

                            #Update Total Schedule
                            machine_available_time = {k: 0 for k in range(n_machines)}
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
