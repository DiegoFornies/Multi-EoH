
def heuristic(input_data):
    """Combines greedy makespan and SPT with local search for balance."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Initialize schedule
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    # Phase 1: Hybrid Makespan & SPT Minimization
    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    while available_operations:
        best_operation = None
        best_machine = None
        earliest_start_time = float('inf')
        shortest_processing_time = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                # Primary criteria: Minimize start time
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    shortest_processing_time = processing_time
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)
                # Secondary criteria: SPT for tie-breaking
                elif start_time == earliest_start_time and processing_time < shortest_processing_time:
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

    # Phase 2: Balance Improvement (Local Search - Swap Machines)
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
    
    best_schedule = schedule
    best_objectives = objective_functions(best_schedule)

    # Improve machine balance by swapping machines for each operation
    for job_id in range(1, n_jobs + 1):
        for op_idx in range(len(schedule[job_id])):
            operation = schedule[job_id][op_idx]
            original_machine = operation['Assigned Machine']
            original_start_time = operation['Start Time']
            original_end_time = operation['End Time']
            original_processing_time = operation['Processing Time']

            #Try to find a better machine by switching machines
            machines = jobs[job_id][op_idx][0]
            times = jobs[job_id][op_idx][1]

            for machine_idx, machine in enumerate(machines):
                if machine != original_machine:
                    processing_time = times[machine_idx]
                    machine_available_time_copy = machine_available_time.copy()
                    job_completion_time_copy = job_completion_time.copy()

                    # Calculate start and end times if the machine is changed
                    start_time = max(machine_available_time_copy[machine], job_completion_time_copy[job_id])
                    end_time = start_time + processing_time

                    # Temporarily update to see the result
                    schedule[job_id][op_idx]['Assigned Machine'] = machine
                    schedule[job_id][op_idx]['Start Time'] = start_time
                    schedule[job_id][op_idx]['End Time'] = end_time
                    schedule[job_id][op_idx]['Processing Time'] = processing_time

                    # Recalculate job completion time and machine availabilty
                    machine_available_time_copy[machine] = end_time
                    job_completion_time_copy[job_id] = end_time
                    
                    current_obj = objective_functions(schedule)
                    
                    if current_obj['Balance'] < best_objectives['Balance']:
                        best_objectives = current_obj
                        best_schedule = {k: [op.copy() for op in v] for k, v in schedule.items()}
                        
                        #Refine complete re-scheduling to incorporate effect on the entire solution
                        machine_available_time = {m: 0 for m in range(n_machines)}
                        job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

                        for job_id_re in range(1, n_jobs+1):
                            for op_idx_re in range(len(schedule[job_id_re])):
                                machine_re = schedule[job_id_re][op_idx_re]['Assigned Machine']
                                processing_time_re = schedule[job_id_re][op_idx_re]['Processing Time']
                                
                                start_time_re = max(machine_available_time[machine_re], job_completion_time[job_id_re])
                                end_time_re = start_time_re + processing_time_re
                                
                                schedule[job_id_re][op_idx_re]['Start Time'] = start_time_re
                                schedule[job_id_re][op_idx_re]['End Time'] = end_time_re
                                
                                machine_available_time[machine_re] = end_time_re
                                job_completion_time[job_id_re] = end_time_re

                    else:
                        # Revert changes if balance isn't improved
                        schedule[job_id][op_idx]['Assigned Machine'] = original_machine
                        schedule[job_id][op_idx]['Start Time'] = original_start_time
                        schedule[job_id][op_idx]['End Time'] = original_end_time
                        schedule[job_id][op_idx]['Processing Time'] = original_processing_time
    
    return best_schedule
