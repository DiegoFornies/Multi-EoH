
def heuristic(input_data):
    """Hybrid heuristic: Combines makespan & machine reassignment."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    eligible_operations = []
    for job in range(1, n_jobs + 1):
        eligible_operations.append((job, 0))

    while eligible_operations:
        best_operation = None
        earliest_end_time = float('inf')

        for job, op_idx in eligible_operations:
            machines, times = jobs[job][op_idx]
            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time

                if end_time < earliest_end_time:
                    earliest_end_time = end_time
                    best_operation = (job, op_idx, machine, processing_time)

        job, op_idx, assigned_machine, processing_time = best_operation
        start_time = max(machine_available_time[assigned_machine], job_completion_time[job])
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[assigned_machine] = end_time
        job_completion_time[job] = end_time
        eligible_operations.remove((job, op_idx))

        if op_idx + 1 < len(jobs[job]):
            eligible_operations.append((job, op_idx + 1))
    
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
    
    # Machine Reassignment to improve load balance
    for job_id in range(1, n_jobs + 1):
        for op_idx in range(len(schedule[job_id])):
            original_machine = schedule[job_id][op_idx]['Assigned Machine']
            machines = jobs[job_id][op_idx][0]
            
            for new_machine in machines:
                if new_machine != original_machine:
                    temp_schedule = {k: [op.copy() for op in v] for k, v in schedule.items()}
                    
                    # Correctly assign the new machine
                    temp_schedule[job_id][op_idx]['Assigned Machine'] = new_machine

                    #Get processing time from correct machine
                    processing_time = jobs[job_id][op_idx][1][machines.index(new_machine)]
                    temp_schedule[job_id][op_idx]['Processing Time'] = processing_time
                    
                    # Recalculate start and end times based on updated machine assignments
                    temp_machine_available_time = {m: 0 for m in range(n_machines)}
                    temp_job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

                    new_schedule = {job_id_re: [] for job_id_re in range(1, n_jobs + 1)}

                    is_feasible = True  # Flag for feasibility

                    for job_id_re in range(1, n_jobs + 1):
                        for op_idx_re in range(len(jobs[job_id_re])):

                            possible_machines = jobs[job_id_re][op_idx_re][0]
                            current_machine = temp_schedule[job_id_re][op_idx_re]['Assigned Machine']

                            if current_machine not in possible_machines:
                                is_feasible = False
                                break

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

                        if not is_feasible:
                            break
                    
                    if is_feasible:
                        new_objectives = objective_functions(new_schedule)
                    
                        if new_objectives['Balance'] < best_objectives['Balance']:
                            best_schedule = {k: [op.copy() for op in v] for k, v in new_schedule.items()}
                            best_objectives = new_objectives
                            schedule = new_schedule
    return best_schedule
