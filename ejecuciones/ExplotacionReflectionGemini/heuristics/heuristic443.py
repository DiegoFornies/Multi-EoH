
def heuristic(input_data):
    """Combines greedy, SPT, and local search to minimize makespan and balance load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job_id: [] for job_id in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    available_operations = [(job_id, 0) for job_id in range(1, n_jobs + 1)]

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
                score = end_time + machine_load[machine] * 0.1 # Load balancing

                if score < earliest_end_time:
                    earliest_end_time = score
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)

        if best_operation:
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

    # Local Search: Reassign operations to balance machine load
    def objective_functions(current_schedule):
        machine_load_obj = {m: 0 for m in range(n_machines)}
        for job_id in current_schedule:
            for operation in current_schedule[job_id]:
                machine_load_obj[operation['Assigned Machine']] += operation['Processing Time']

        makespan_obj = 0
        for job_id in current_schedule:
            if current_schedule[job_id]:
                makespan_obj = max(makespan_obj, current_schedule[job_id][-1]['End Time'])

        total_load = sum(machine_load_obj.values())
        n_machines_used = len([m for m in machine_load_obj if machine_load_obj[m] > 0])

        if n_machines_used > 0:
            balance_obj = sum([(machine_load_obj[m] - (total_load / n_machines_used)) ** 2 for m in machine_load_obj if machine_load_obj[m] > 0]) / n_machines_used
        else:
            balance_obj = 0

        separation_obj = 0  # Placeholder

        return {'Makespan': makespan_obj, 'Separation': separation_obj, 'Balance': balance_obj}

    best_schedule = schedule
    best_objectives = objective_functions(best_schedule)

    for job_id in range(1, n_jobs + 1):
        for op_idx in range(len(schedule[job_id])):
            original_machine = schedule[job_id][op_idx]['Assigned Machine']
            machines = jobs[job_id][op_idx][0]

            for new_machine in machines:
                if new_machine != original_machine:
                    temp_schedule = {job_id_temp: [op.copy() for op in schedule[job_id_temp]] for job_id_temp in range(1, n_jobs + 1)}
                    processing_time = jobs[job_id][op_idx][1][machines.index(new_machine)]

                    # modify the temp schedule operation machine and processing time
                    temp_schedule[job_id][op_idx]['Assigned Machine'] = new_machine
                    temp_schedule[job_id][op_idx]['Processing Time'] = processing_time

                    #Recalculate timing.
                    temp_machine_available_time = {m: 0 for m in range(n_machines)}
                    temp_job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

                    feasible = True
                    for job_id_re in range(1, n_jobs+1):
                        for op_idx_re in range(len(jobs[job_id_re])):
                            machines_re = jobs[job_id_re][op_idx_re][0]

                            if job_id_re == job_id and op_idx_re == op_idx:
                                selected_machine = new_machine
                                processing_time_re = jobs[job_id_re][op_idx_re][1][machines_re.index(new_machine)]
                            else:
                                selected_machine = temp_schedule[job_id_re][op_idx_re]['Assigned Machine']
                                processing_time_re = temp_schedule[job_id_re][op_idx_re]['Processing Time']

                            start_time = max(temp_machine_available_time[selected_machine], temp_job_completion_time[job_id_re])
                            end_time = start_time+processing_time_re
                            temp_schedule[job_id_re][op_idx_re]['Start Time'] = start_time
                            temp_schedule[job_id_re][op_idx_re]['End Time'] = end_time
                            temp_machine_available_time[selected_machine] = end_time
                            temp_job_completion_time[job_id_re] = end_time

                    new_objectives = objective_functions(temp_schedule)

                    if new_objectives['Balance'] < best_objectives['Balance']:
                        best_schedule = temp_schedule
                        best_objectives = new_objectives
                        schedule = temp_schedule
                    elif new_objectives['Makespan'] < best_objectives['Makespan'] and new_objectives['Balance'] == best_objectives['Balance']:
                        best_schedule = temp_schedule
                        best_objectives = new_objectives
                        schedule = temp_schedule

    return best_schedule
