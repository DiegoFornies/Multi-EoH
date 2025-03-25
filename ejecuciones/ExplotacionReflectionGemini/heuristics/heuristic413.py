
def heuristic(input_data):
    """Combines greedy and local search, balances makespan and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    remaining_operations = {j: len(jobs[j]) for j in range(1, n_jobs + 1)}
    scheduled_operations = set()

    operations = []
    for job_id in jobs:
        for op_idx, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, op_data))

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
        min_start_time = float('inf')
        best_machine = None

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data

            # Choose machine considering both start time and machine load
            best_machine_local = -1
            best_start_time_local = float('inf')
            best_time_local = float('inf')
            best_load_local = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + time

                if start_time < best_start_time_local:
                    best_start_time_local = start_time
                    best_time_local = end_time
                    best_machine_local = machine
                    best_load_local = machine_load[machine]
                elif start_time == best_start_time_local:
                    if machine_load[machine] < best_load_local:
                        best_machine_local = machine
                        best_time_local = end_time
                        best_load_local = machine_load[machine]

            if best_start_time_local < min_start_time:
                min_start_time = best_start_time_local
                best_operation = (job_id, op_idx, op_data, best_machine_local, best_start_time_local)

        job_id, op_idx, op_data, machine, start_time = best_operation
        machines, times = op_data
        time = next(t for i, t in enumerate(times) if machines[i] == machine)
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
        job_completion_time[job_id] = end_time
        machine_load[machine] += time
        remaining_operations[job_id] -= 1
        scheduled_operations.add((job_id, op_idx))

    # Local search for improvement (machine reassignment)
    best_schedule = schedule
    best_makespan = float('inf')
    for job in schedule:
      if schedule[job]:
          best_makespan = max(best_makespan,schedule[job][-1]['End Time'])
      
    #Improvement by reassignment
    for job_id in range(1,n_jobs+1):
        if job_id not in schedule:
            continue
        for op_idx in range(len(schedule[job_id])):
            original_machine = schedule[job_id][op_idx]['Assigned Machine']
            machines = jobs[job_id][op_idx][0]
            
            for new_machine in machines:
                if new_machine != original_machine:
                    temp_schedule = {job: [op.copy() for op in schedule[job]] for job in schedule}
                    temp_schedule[job_id][op_idx]['Assigned Machine'] = new_machine
                    
                    processing_time = jobs[job_id][op_idx][1][machines.index(new_machine)]
                    temp_schedule[job_id][op_idx]['Processing Time'] = processing_time
                    
                    #Recalculate start and end times
                    temp_machine_available_time = {m: 0 for m in range(n_machines)}
                    temp_job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
                    
                    is_feasible = True
                    
                    for job_id_re in range(1, n_jobs + 1):
                        if job_id_re not in temp_schedule:
                            continue
                        for op_idx_re in range(len(temp_schedule[job_id_re])):
                            
                            if job_id_re == job_id and op_idx_re == op_idx:
                                machine = new_machine
                                processing_time = jobs[job_id_re][op_idx_re][1][machines.index(new_machine)]
                            else:
                                machine = temp_schedule[job_id_re][op_idx_re]['Assigned Machine']
                                processing_time = temp_schedule[job_id_re][op_idx_re]['Processing Time']
                            
                            start_time = max(temp_machine_available_time[machine], temp_job_completion_time[job_id_re])
                            end_time = start_time + processing_time

                            temp_schedule[job_id_re][op_idx_re]['Start Time'] = start_time
                            temp_schedule[job_id_re][op_idx_re]['End Time'] = end_time

                            temp_machine_available_time[machine] = end_time
                            temp_job_completion_time[job_id_re] = end_time
                            
                    new_makespan = float('inf')
                    for job in temp_schedule:
                      if temp_schedule[job]:
                          new_makespan = max(new_makespan,temp_schedule[job][-1]['End Time'])

                    if new_makespan < best_makespan:
                        best_makespan = new_makespan
                        best_schedule = {job: [op.copy() for op in temp_schedule[job]] for job in temp_schedule}
                        

    return best_schedule
