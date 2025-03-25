
def heuristic(input_data):
    """A two-phase heuristic for FJSSP: minimize makespan then balance."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Initialize schedule
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    # Phase 1: Makespan Minimization (Greedy)
    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

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

    # Phase 2: Balance Improvement (Local Search - Machine Load Balancing)
    for _ in range(5):  # Limited iterations for balance improvement
        for machine in range(n_machines):
            # Find operations assigned to this machine
            operations_on_machine = []
            for job_id in range(1, n_jobs + 1):
                for op_idx, operation in enumerate(schedule[job_id]):
                    if operation['Assigned Machine'] == machine:
                        operations_on_machine.append((job_id, op_idx))

            if len(operations_on_machine) > 1:
                # Try to reassign the operation that causes max machine end time to another machine
                max_end_time = 0
                worst_operation = None
                for job_id, op_idx in operations_on_machine:
                    if schedule[job_id][op_idx]['End Time'] > max_end_time:
                        max_end_time = schedule[job_id][op_idx]['End Time']
                        worst_operation = (job_id, op_idx)
                
                job_id, op_idx = worst_operation
                current_machine = schedule[job_id][op_idx]['Assigned Machine']
                current_start_time = schedule[job_id][op_idx]['Start Time']
                current_processing_time = schedule[job_id][op_idx]['Processing Time']
                
                original_end_time = schedule[job_id][op_idx]['End Time']
                
                #Find feasible alternative machine for this operation
                machines, times = jobs[job_id][op_idx]
                
                best_alternative_machine = None
                best_alternative_start_time = float('inf')
                
                for alt_machine_idx, alt_machine in enumerate(machines):
                    if alt_machine != current_machine:
                        alt_processing_time = times[alt_machine_idx]
                        alt_start_time = max(machine_available_time[alt_machine], job_completion_time[job_id])
                        
                        if alt_start_time < best_alternative_start_time:
                            best_alternative_start_time = alt_start_time
                            best_alternative_machine = alt_machine
                            best_alt_processing_time = alt_processing_time
                            
                # If a better machine is found, reassign operation from current machine
                if best_alternative_machine is not None:

                    # Reassign this operation to the new machine
                    # Update the schedule, update machime_available_time, update job_completion_time,
                    
                    #Update Job Completetion time (BEFORE REMOVE)
                    job_completion_time[job_id] -= original_end_time-current_start_time
                                        
                    schedule[job_id][op_idx]['Assigned Machine'] = best_alternative_machine
                    schedule[job_id][op_idx]['Start Time'] = best_alternative_start_time
                    schedule[job_id][op_idx]['End Time'] = best_alternative_start_time + best_alt_processing_time
                    schedule[job_id][op_idx]['Processing Time'] = best_alt_processing_time

                    # Update machine_available_time
                    machine_available_time[current_machine] = 0
                    for j_id in range(1, n_jobs+1):
                        for o_idx, operation in enumerate(schedule[j_id]):
                            if operation['Assigned Machine'] == current_machine:
                                machine_available_time[current_machine] = max(machine_available_time[current_machine], operation['End Time'])
                    machine_available_time[best_alternative_machine] = max(machine_available_time[best_alternative_machine],schedule[job_id][op_idx]['End Time'])
                    # Update Job Completetion time (AFTER ADD)
                    job_completion_time[job_id] = schedule[job_id][op_idx]['End Time'] if schedule[job_id][op_idx]['End Time'] > job_completion_time[job_id] else job_completion_time[job_id]  
                                       

    return schedule
