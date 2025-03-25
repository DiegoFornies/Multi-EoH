
def heuristic(input_data):
    """Greedy makespan with balance improvement and local search."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job_id: [] for job_id in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    available_operations = [(job_id, 0) for job_id in range(1, n_jobs + 1)]

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

    # Local Search : Swap operations within the same job
    for job_id in range(1,n_jobs+1):
        if len(schedule[job_id])>1:
            for i in range(len(schedule[job_id])-1):
                for j in range(i+1, len(schedule[job_id])):

                    original_schedule = {job_id: [op.copy() for op in schedule[job_id]] for job_id in schedule}
                    original_obj = objective_functions(original_schedule)
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
                    machine_available_time_temp = {m: 0 for m in range(n_machines)}
                    job_completion_time_temp = {j: 0 for j in range(1, n_jobs + 1)}

                    current_job_schedule = []
                    
                    #Reschedule for current job
                    for op_idx in range(len(temp_schedule[job_id])):
                        machine = temp_schedule[job_id][op_idx]['Assigned Machine']
                        processing_time = temp_schedule[job_id][op_idx]['Processing Time']
                        
                        start_time = max(machine_available_time_temp[machine], job_completion_time_temp[job_id])
                        end_time = start_time + processing_time
                        
                        temp_schedule[job_id][op_idx]['Start Time'] = start_time
                        temp_schedule[job_id][op_idx]['End Time'] = end_time
                        
                        machine_available_time_temp[machine] = end_time
                        job_completion_time_temp[job_id] = end_time
                        current_job_schedule.append(temp_schedule[job_id][op_idx])
                        
                    #Update total schedule
                    temp_schedule_complete = {job_id_all: [op.copy() for op in schedule[job_id_all]] for job_id_all in schedule}
                    temp_schedule_complete[job_id] = current_job_schedule
                    new_objectives = objective_functions(temp_schedule_complete)
                    
                    if new_objectives['Makespan'] < best_objectives['Makespan'] or new_objectives['Balance'] < best_objectives['Balance']:
                        schedule = temp_schedule_complete
                        best_schedule = schedule
                        best_objectives = new_objectives
    return best_schedule
