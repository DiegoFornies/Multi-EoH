
def heuristic(input_data):
    """Hybrid heuristic: Min makespan initially, refine for balance."""
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

    while available_operations:
        best_operation = None
        best_machine = None
        earliest_end_time = float('inf') # Changed from start to end

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < earliest_end_time: #find min end time to minimize makespan
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

    # Refine for balance: try swapping operations between machines
    # for each operation to improve machine load balance

    for job_id in range(1, n_jobs + 1):
        for op_idx in range(len(schedule[job_id])):
            operation = schedule[job_id][op_idx]
            original_machine = operation['Assigned Machine']
            original_start_time = operation['Start Time']
            original_end_time = operation['End Time']
            original_processing_time = operation['Processing Time']

            machines, times = jobs[job_id][op_idx]
            
            for machine_idx, machine in enumerate(machines):
                if machine != original_machine:
                    processing_time = times[machine_idx]
                    
                    # Calculate potential start time on the new machine
                    start_time = max(machine_available_time[machine], job_completion_time[job_id])
                    end_time = start_time + processing_time

                    # Check feasibility: No overlap with existing operations on the new machine
                    overlap = False
                    for other_job_id in range(1, n_jobs + 1):
                         for other_op in schedule[other_job_id]:
                            if other_op['Assigned Machine'] == machine and \
                               start_time < other_op['End Time'] and \
                               end_time > other_op['Start Time'] and (job_id!= other_job_id or op_idx+1 != other_op['Operation']):
                                overlap = True
                                break
                         if overlap:
                            break

                    if not overlap:
                        # Calculate the original machine load
                        original_load_before = 0
                        for job_id_temp in range(1, n_jobs + 1):
                            for operation_temp in schedule[job_id_temp]:
                                if operation_temp['Assigned Machine'] == original_machine:
                                    original_load_before += operation_temp['Processing Time']

                        # Calculate the load after the hypothetical swap
                        original_load_after = original_load_before - original_processing_time
                        
                        #Calculate the new machine load
                        new_machine_load_before = 0
                        for job_id_temp in range(1, n_jobs + 1):
                            for operation_temp in schedule[job_id_temp]:
                                if operation_temp['Assigned Machine'] == machine:
                                    new_machine_load_before += operation_temp['Processing Time']
                                    
                        new_machine_load_after = new_machine_load_before + processing_time
                        
                        #if the swap reduces the standard deviation of the loads, make the swap
                        loads = []
                        for m in range(n_machines):
                            load = 0
                            for job_id_temp in range(1, n_jobs + 1):
                                for operation_temp in schedule[job_id_temp]:
                                    if operation_temp['Assigned Machine'] == m:
                                        load += operation_temp['Processing Time']
                            loads.append(load)
                        import numpy as np
                        original_std = np.std(loads)
                        
                        temp_schedule = {}
                        for k, v in schedule.items():
                            temp_schedule[k] = [d.copy() for d in v]
                        temp_schedule[job_id][op_idx]['Assigned Machine'] = machine
                        temp_schedule[job_id][op_idx]['Start Time'] = start_time
                        temp_schedule[job_id][op_idx]['End Time'] = end_time
                        temp_schedule[job_id][op_idx]['Processing Time'] = processing_time
                        
                        temp_loads = []
                        for m in range(n_machines):
                            load = 0
                            for job_id_temp in range(1, n_jobs + 1):
                                for operation_temp in temp_schedule[job_id_temp]:
                                    if operation_temp['Assigned Machine'] == m:
                                        load += operation_temp['Processing Time']
                            temp_loads.append(load)
                            
                        temp_std = np.std(temp_loads)

                        if temp_std < original_std:                            
                            # Update the schedule with the swapped operation
                            operation['Assigned Machine'] = machine
                            operation['Start Time'] = start_time
                            operation['End Time'] = end_time
                            operation['Processing Time'] = processing_time

                            # Update machine available times and job completion times
                            machine_available_time = {m: 0 for m in range(n_machines)}
                            job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
                            for job_id_temp in range(1, n_jobs + 1):
                                for operation_temp in schedule[job_id_temp]:
                                    machine_available_time[operation_temp['Assigned Machine']] = max(machine_available_time[operation_temp['Assigned Machine']], operation_temp['End Time'])
                                    job_completion_time[job_id_temp] = max(job_completion_time[job_id_temp], operation_temp['End Time'])
                                    
                            break  # Swap done, check next operation

    return schedule
