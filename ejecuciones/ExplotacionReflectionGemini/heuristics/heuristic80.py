
def heuristic(input_data):
    """Hybrid heuristic: makespan-focused initial schedule, then balance."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    # Makespan-focused initial schedule (SPT-like)
    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    while available_operations:
        best_operation = None
        best_machine = None
        shortest_processing_time = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                if processing_time < shortest_processing_time:
                    shortest_processing_time = processing_time
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

    # Balancing pass (iterative improvement)
    for _ in range(2):  # Number of balancing iterations
        for job_id in range(1, n_jobs + 1):
            for op_idx in range(len(schedule[job_id])):
                current_machine = schedule[job_id][op_idx]['Assigned Machine']
                current_start_time = schedule[job_id][op_idx]['Start Time']
                current_end_time = schedule[job_id][op_idx]['End Time']
                current_processing_time = schedule[job_id][op_idx]['Processing Time']
                
                original_end_time = current_end_time

                machines, times = jobs[job_id][op_idx]
                
                best_alternative_machine = None
                best_alternative_start_time = float('inf')
                
                for machine_idx, machine in enumerate(machines):
                    if machine != current_machine:
                        processing_time = times[machine_idx]
                        start_time = max(machine_available_time[machine], job_completion_time[job_id])
                        
                        if start_time < best_alternative_start_time:
                            best_alternative_start_time = start_time
                            best_alternative_machine = (machine, processing_time)
                
                if best_alternative_machine:
                    machine, processing_time = best_alternative_machine
                    start_time = max(machine_available_time[machine], job_completion_time[job_id])
                    end_time = start_time + processing_time
                    
                    #Check for overlapping operations on machines
                    overlap = False
                    for job_id_other in range(1, n_jobs + 1):
                        for op_idx_other in range(len(schedule[job_id_other])):
                            if schedule[job_id_other][op_idx_other]['Assigned Machine'] == machine:
                                start_other = schedule[job_id_other][op_idx_other]['Start Time']
                                end_other = schedule[job_id_other][op_idx_other]['End Time']
                                if (start_time < end_other and end_time > start_other):
                                    overlap = True
                                    break
                        if overlap:
                            break
                    
                    if not overlap:
                        machine_available_time[current_machine] -= current_processing_time
                        machine_available_time[machine] = end_time
                        job_completion_time[job_id] = end_time
                        
                        # update schedule
                        schedule[job_id][op_idx]['Assigned Machine'] = machine
                        schedule[job_id][op_idx]['Start Time'] = start_time
                        schedule[job_id][op_idx]['End Time'] = end_time
                        schedule[job_id][op_idx]['Processing Time'] = processing_time
                        
                        # Update job completion times based on new schedule
                        job_completion_time[job_id] = 0
                        for operation in schedule[job_id]:
                            job_completion_time[job_id] = max(job_completion_time[job_id],operation['End Time'])

                        # Update machine available times based on new schedule
                        machine_available_time = {m: 0 for m in range(n_machines)}
                        for job_id_update in range(1, n_jobs + 1):
                            for operation in schedule[job_id_update]:
                                machine_available_time[operation['Assigned Machine']] = max(machine_available_time[operation['Assigned Machine']], operation['End Time'])

    return schedule
