
def heuristic(input_data):
    """Schedules jobs using a combination of SPT, machine load balancing, and local search."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    remaining_operations = {j: len(jobs_data[j]) for j in range(1, n_jobs + 1)}
    scheduled_operations = set()

    operations = []
    for job_id in jobs_data:
        for op_idx, op_data in enumerate(jobs_data[job_id]):
            operations.append((job_id, op_idx, op_data))

    while any(remaining_operations[job] > 0 for job in range(1, n_jobs + 1)):
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
            if job_id not in jobs_data:
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
        min_makespan_increase = float('inf')

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                end_time = start_time + time

                makespan_increase = max(0, end_time - max(machine_available_time.values())) # Estimate makespan increase

                if makespan_increase < min_makespan_increase:
                    min_makespan_increase = makespan_increase
                    best_operation = (job_id, op_idx, op_data, machine, start_time, time, end_time)
                elif makespan_increase == min_makespan_increase:
                    # Tie-breaker: favour machine with less load
                    if machine_load[machine] < machine_load[best_operation[3]]:
                         best_operation = (job_id, op_idx, op_data, machine, start_time, time, end_time)

        if best_operation is None:
            break

        job_id, op_idx, op_data, machine, start_time, time, end_time = best_operation
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

    # Local search
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

    #Improvement by reassignment
    for job_id in range(1,n_jobs+1):
        for op_idx in range(len(schedule[job_id])):
            original_schedule = {job_id: [op.copy() for op in schedule[job_id]]}
            original_obj = objective_functions(schedule)
            
            original_machine = schedule[job_id][op_idx]['Assigned Machine']
            
            machines = jobs_data[job_id][op_idx][0]
            
            for new_machine in machines:
                if new_machine != original_machine:
                    temp_schedule = {job_id: [op.copy() for op in schedule[job_id]]}
                    temp_schedule[job_id][op_idx]['Assigned Machine'] = new_machine
                    
                    processing_time = jobs_data[job_id][op_idx][1][machines.index(new_machine)]
                    temp_schedule[job_id][op_idx]['Processing Time'] = processing_time
                    
                    # Update the start and end times based on the new machine assignments.
                    # Recalculate the entire schedule to ensure feasibility.
                    temp_machine_available_time = {m: 0 for m in range(n_machines)}
                    temp_job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
                    is_feasible = True
                    
                    new_schedule = {}
                    for job_id_re in range(1, n_jobs + 1):
                        new_schedule[job_id_re] = []
                        for op_idx_re in range(len(jobs_data[job_id_re])):
                            
                            if job_id_re == job_id and op_idx_re == op_idx:
                                machine = new_machine
                                processing_time = jobs_data[job_id_re][op_idx_re][1][machines.index(new_machine)]

                            else:
                                #Find original assigned machine and its processing time
                                orig_machine = schedule[job_id_re][op_idx_re]['Assigned Machine']
                                orig_processing_time = schedule[job_id_re][op_idx_re]['Processing Time']
                                machine = orig_machine
                                processing_time = orig_processing_time
                                
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

                    if new_objectives['Balance'] < best_objectives['Balance'] and new_objectives['Makespan'] <= best_objectives['Makespan']:
                        best_schedule = new_schedule
                        best_objectives = new_objectives
                        schedule = new_schedule

    return best_schedule
