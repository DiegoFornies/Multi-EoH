
def heuristic(input_data):
    """Heuristic for FJSSP: Greedy makespan + balance refinement."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    # Initialize schedule
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    # Greedy makespan initialization
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
        machine_load[machine] += processing_time
        available_operations.remove((job_id, op_idx))

        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))

    # Balance refinement (simple local search - machine reassignment)
    for job_id in range(1, n_jobs + 1):
        for op_idx in range(len(schedule[job_id])):
            original_machine = schedule[job_id][op_idx]['Assigned Machine']
            original_start_time = schedule[job_id][op_idx]['Start Time']
            original_end_time = schedule[job_id][op_idx]['End Time']
            original_processing_time = schedule[job_id][op_idx]['Processing Time']

            machines, times = jobs[job_id][op_idx]
            best_balance = machine_load[original_machine]
            best_machine = original_machine
            best_start_time = original_start_time
            
            for machine_idx, machine in enumerate(machines):
                if machine != original_machine:
                    processing_time = times[machine_idx]
                    
                    # Calculate potential start time considering machine availability and job dependencies
                    start_time = max(machine_available_time[machine], job_completion_time[job_id] - original_processing_time + schedule[job_id][op_idx]['Processing Time'])
                    
                    potential_load = machine_load[original_machine] - original_processing_time
                    
                    if potential_load < best_balance :
                         best_balance = potential_load
                         best_machine = machine
                         best_start_time = start_time


            if best_machine != original_machine:
                schedule[job_id][op_idx]['Assigned Machine'] = best_machine
                schedule[job_id][op_idx]['Start Time'] = best_start_time
                schedule[job_id][op_idx]['End Time'] = best_start_time + original_processing_time


                machine_load[original_machine] -= original_processing_time
                machine_load[best_machine] += original_processing_time
                machine_available_time[best_machine] = best_start_time + original_processing_time
    return schedule
