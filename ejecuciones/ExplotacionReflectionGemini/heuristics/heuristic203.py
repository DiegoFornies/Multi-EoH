
def heuristic(input_data):
    """Schedules jobs, balancing makespan and machine load. Combines SPT, machine load, and local search."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, 1 + n_jobs)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, 1 + n_jobs)}
    machine_load = {m: 0 for m in range(n_machines)}

    remaining_operations = {j: len(jobs_data[j]) for j in range(1, 1 + n_jobs)}
    scheduled_operations = set()

    operations = []
    for job_id in jobs_data:
        for op_idx, op_data in enumerate(jobs_data[job_id]):
            operations.append((job_id, op_idx, op_data))

    while any(remaining_operations[job] > 0 for job in range(1, 1 + n_jobs)):
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
            best_machine = -1
            best_start_time = float('inf')
            best_processing_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                end_time = start_time + time
                makespan_increase = end_time - machine_available_time[machine] if end_time > machine_available_time[machine] else 0

                # Prioritize minimizing makespan increase, then balance machine load
                if makespan_increase < min_makespan_increase:
                    min_makespan_increase = makespan_increase
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = time
                elif makespan_increase == min_makespan_increase and machine_load[machine] < (sum(machine_load.values()) / n_machines if n_machines > 0 else 0):
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = time

            if best_machine != -1:
                best_operation = (job_id, op_idx, best_machine, best_start_time, best_processing_time)
                break  # Stop after finding the best operation

        if best_operation:
            job_id, op_idx, best_machine, best_start_time, best_processing_time = best_operation
            op_num = op_idx + 1
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_last_end_time[job_id] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            remaining_operations[job_id] -= 1
            scheduled_operations.add((job_id, op_idx))

    # Local search for balancing (simplified swap)
    for job_id in range(1, n_jobs + 1):
        if len(schedule[job_id]) > 1:
            for i in range(len(schedule[job_id]) - 1):
                for j in range(i + 1, len(schedule[job_id])):
                    original_machine_i = schedule[job_id][i]['Assigned Machine']
                    original_machine_j = schedule[job_id][j]['Assigned Machine']
                    
                    #Check possible machines
                    machines_i = jobs_data[job_id][i][0]
                    machines_j = jobs_data[job_id][j][0]
                    
                    if original_machine_j in machines_i and original_machine_i in machines_j:
                        #Swap machines
                        schedule[job_id][i]['Assigned Machine'] = original_machine_j
                        schedule[job_id][j]['Assigned Machine'] = original_machine_i

                        #Recalculate
                        machine_available_time = {m: 0 for m in range(n_machines)}
                        job_last_end_time = {j: 0 for j in range(1, 1 + n_jobs)}

                        valid_swap = True
                        for op_idx in range(len(schedule[job_id])):
                            machine = schedule[job_id][op_idx]['Assigned Machine']
                            proc_time_list = jobs_data[job_id][op_idx]['1']
                            proc_time_index = jobs_data[job_id][op_idx]['0'].index(machine)
                            proc_time = jobs_data[job_id][op_idx]['1'][proc_time_index]
                            start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                            end_time = start_time + proc_time

                            schedule[job_id][op_idx]['Start Time'] = start_time
                            schedule[job_id][op_idx]['End Time'] = end_time
                            schedule[job_id][op_idx]['Processing Time'] = proc_time

                            machine_available_time[machine] = end_time
                            job_last_end_time[job_id] = end_time

                        #Check makespan
                        makespan_before = max(op['End Time'] for job in schedule for op in schedule[job])
                        #Undo if makespan increased
                        makespan_after = max(op['End Time'] for job in schedule for op in schedule[job])

                        if makespan_after > makespan_before :
                            schedule[job_id][i]['Assigned Machine'] = original_machine_i
                            schedule[job_id][j]['Assigned Machine'] = original_machine_j
                            
                            machine_available_time = {m: 0 for m in range(n_machines)}
                            job_last_end_time = {j: 0 for j in range(1, 1 + n_jobs)}

                            for op_idx in range(len(schedule[job_id])):
                                machine = schedule[job_id][op_idx]['Assigned Machine']
                                proc_time_list = jobs_data[job_id][op_idx]['1']
                                proc_time_index = jobs_data[job_id][op_idx]['0'].index(machine)
                                proc_time = jobs_data[job_id][op_idx]['1'][proc_time_index]
                                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                                end_time = start_time + proc_time

                                schedule[job_id][op_idx]['Start Time'] = start_time
                                schedule[job_id][op_idx]['End Time'] = end_time
                                schedule[job_id][op_idx]['Processing Time'] = proc_time

                                machine_available_time[machine] = end_time
                                job_last_end_time[job_id] = end_time
                                
    return schedule
