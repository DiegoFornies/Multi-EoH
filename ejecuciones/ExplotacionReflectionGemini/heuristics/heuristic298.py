
def heuristic(input_data):
    """Greedy makespan schedule with local search (machine reassignment)
       to improve machine load balance."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job_id: [] for job_id in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Phase 1: Greedy Makespan Minimization
    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, op_data))

    while any(len(schedule[job_id]) < len(jobs[job_id]) for job_id in range(1, n_jobs + 1)):
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
            if len(schedule[job_id]) == op_idx:
                eligible_operations.append((job_id, op_idx, op_data))

        if not eligible_operations:
            break

        best_operation = None
        min_end_time = float('inf')

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time
                if end_time < min_end_time:
                    min_end_time = end_time
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

        else:
            break

    # Phase 2: Local Search for Balance Improvement
    def calculate_machine_load(current_schedule):
        machine_load = {m: 0 for m in range(n_machines)}
        for job_id in current_schedule:
            for operation in current_schedule[job_id]:
                machine_load[operation['Assigned Machine']] += operation['Processing Time']
        return machine_load

    def calculate_makespan(current_schedule):
        makespan = 0
        for job_id in current_schedule:
            if current_schedule[job_id]:
                makespan = max(makespan, current_schedule[job_id][-1]['End Time'])
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
    
    # Iterate through operations and try reassignment
    for job_id in range(1, n_jobs + 1):
        for op_idx in range(len(schedule[job_id])):
            original_machine = schedule[job_id][op_idx]['Assigned Machine']
            machines, times = jobs[job_id][op_idx]

            for i, new_machine in enumerate(machines):
                if new_machine != original_machine:

                    temp_schedule = {k: [op.copy() for op in v] for k, v in schedule.items()} #deep copy

                    processing_time = times[i]
                    temp_schedule[job_id][op_idx]['Assigned Machine'] = new_machine
                    temp_schedule[job_id][op_idx]['Processing Time'] = processing_time
                    
                    # Recalculate schedule after reassignment
                    temp_machine_available_time = {m: 0 for m in range(n_machines)}
                    temp_job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
                    new_schedule = {job_id_re: [] for job_id_re in range(1, n_jobs + 1)}
                    
                    for job_id_re in range(1,n_jobs +1):
                        for op_idx_re in range(len(jobs[job_id_re])):
                            machines_re, times_re = jobs[job_id_re][op_idx_re]
                            
                            if job_id_re == job_id and op_idx_re == op_idx:
                                assigned_machine = new_machine
                                proc_time = processing_time

                            else:
                                assigned_machine = temp_schedule[job_id_re][op_idx_re]['Assigned Machine']
                                proc_time = temp_schedule[job_id_re][op_idx_re]['Processing Time']
                            
                            start_time = max(temp_machine_available_time[assigned_machine], temp_job_completion_time[job_id_re])
                            end_time = start_time + proc_time

                            new_schedule[job_id_re].append({
                                'Operation': op_idx_re + 1,
                                'Assigned Machine': assigned_machine,
                                'Start Time': start_time,
                                'End Time': end_time,
                                'Processing Time': proc_time
                            })
                            
                            temp_machine_available_time[assigned_machine] = end_time
                            temp_job_completion_time[job_id_re] = end_time
                    
                    new_objectives = objective_functions(new_schedule)
                    
                    if new_objectives['Balance'] < best_objectives['Balance']:
                        best_schedule = {k: [op.copy() for op in v] for k, v in new_schedule.items()}
                        best_objectives = new_objectives
                        schedule = new_schedule

    return best_schedule
