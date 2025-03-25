
def heuristic(input_data):
    """
    Hybrid heuristic: Greedy makespan minimization + balance refinement.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    # Greedy makespan minimization (Phase 1)
    while available_operations:
        best_operation = None
        best_machine = None
        earliest_end_time = float('inf')  # Change from start to end

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < earliest_end_time:  # Consider end time
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

    # Balance refinement (Phase 2): machine load balancing.
    # Simple machine load refinement by reassigning the least loaded machine
    machine_load = {m: 0 for m in range(n_machines)}
    for job_id in schedule:
        for operation in schedule[job_id]:
            machine_load[operation['Assigned Machine']] += operation['Processing Time']

    for job_id in range(1, n_jobs + 1):
        for op_idx in range(len(jobs[job_id])):
            operation = schedule[job_id][op_idx]
            original_machine = operation['Assigned Machine']
            machines, times = jobs[job_id][op_idx]

            best_machine = original_machine
            best_time = operation['Processing Time']
            best_load = machine_load[original_machine] # initial benchmark

            for i, machine in enumerate(machines):
                processing_time = times[i]

                temp_machine_load = machine_load.copy()
                temp_machine_load[original_machine] -= operation['Processing Time'] # subtract current
                temp_machine_load[machine] += processing_time # add trial

                # Objective: balance machine load. Lower the SD the better
                load_sd = (sum([(temp_machine_load[machine]-sum(temp_machine_load.values())/n_machines)**2 for machine in temp_machine_load.keys()])/(n_machines))**0.5
                if load_sd < (sum([(machine_load[machine]-sum(machine_load.values())/n_machines)**2 for machine in machine_load.keys()])/(n_machines))**0.5:
                    best_machine = machine
                    best_time = processing_time

            if best_machine != original_machine: #assign to the better machine
                machine_load[original_machine] -= operation['Processing Time']
                machine_load[best_machine] += best_time
                operation['Assigned Machine'] = best_machine
                operation['Processing Time'] = best_time

                # Recalculate start and end times for the job
                job_start_time = 0
                for i in range(len(schedule[job_id])):
                    operation = schedule[job_id][i]
                    machine = operation['Assigned Machine']
                    processing_time = operation['Processing Time']
                    start_time = max(machine_available_time[machine], job_start_time)
                    end_time = start_time + processing_time
                    operation['Start Time'] = start_time
                    operation['End Time'] = end_time
                    job_start_time = end_time
                    machine_available_time[machine] = end_time # update machine

    return schedule
