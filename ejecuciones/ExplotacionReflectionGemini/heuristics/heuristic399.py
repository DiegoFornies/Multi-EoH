
def heuristic(input_data):
    """Heuristic for FJSSP: Makespan minimization + balance refinement."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    scheduled_operations = set()

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
        machine_load[machine] += processing_time  # Update machine load
        available_operations.remove((job_id, op_idx))

        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))

    # Balance Refinement (Simple Load Balancing)
    max_load = max(machine_load.values())
    for job_id in range(1, n_jobs + 1):
        for i in range(len(schedule[job_id])):
            operation = schedule[job_id][i]
            machine = operation['Assigned Machine']
            op_idx = operation['Operation'] - 1 #back to index
            current_processing_time = operation['Processing Time']
            
            machines, times = jobs[job_id][op_idx]
            
            original_start_time = operation['Start Time']
            
            for alt_machine_idx, alt_machine in enumerate(machines):
                if alt_machine != machine:
                    alt_processing_time = times[alt_machine_idx]
                    
                    temp_machine_load = machine_load.copy()
                    temp_machine_load[machine] -= current_processing_time
                    temp_machine_load[alt_machine] += alt_processing_time

                    if max(temp_machine_load.values()) < max_load:
                        
                        start_time = max(machine_available_time[alt_machine] if alt_machine in machine_available_time else 0, job_completion_time[job_id])
                        end_time = start_time + alt_processing_time
                                                    
                        schedule[job_id][i]['Assigned Machine'] = alt_machine
                        schedule[job_id][i]['Start Time'] = start_time
                        schedule[job_id][i]['End Time'] = end_time
                        schedule[job_id][i]['Processing Time'] = alt_processing_time

                        machine_load[machine] -= current_processing_time
                        machine_load[alt_machine] += alt_processing_time
                        machine_available_time[machine] = original_start_time+current_processing_time
                        machine_available_time[alt_machine] = end_time
                        job_completion_time[job_id] = end_time
                        
                        max_load = max(machine_load.values())

    return schedule
