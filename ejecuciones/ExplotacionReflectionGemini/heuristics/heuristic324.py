
def heuristic(input_data):
    """Combines earliest machine availability with local search to balance load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    eligible_operations = []
    for job, operations in jobs.items():
        eligible_operations.append((job, 0))  # (job, operation_index)

    while eligible_operations:
        # Select the next operation based on earliest machine availability
        best_operation = None
        earliest_end_time = float('inf')

        for job, op_idx in eligible_operations:
            machines, times = jobs[job][op_idx]

            # find the machine available earliest for the operation
            best_machine, min_end_time = -1, float('inf')
            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine

            if min_end_time < earliest_end_time:
                earliest_end_time = min_end_time
                best_operation = (job, op_idx, best_machine, times[machines.index(best_machine)])

        # Schedule the selected operation
        job, op_idx, assigned_machine, processing_time = best_operation
        start_time = max(machine_available_time[assigned_machine], job_completion_time[job])
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine availability and job completion time
        machine_available_time[assigned_machine] = end_time
        job_completion_time[job] = end_time

        # Remove the scheduled operation from eligible operations
        eligible_operations.remove((job, op_idx))

        # Add the next operation of the same job to eligible operations, if any
        if op_idx + 1 < len(jobs[job]):
            eligible_operations.append((job, op_idx + 1))

    # Phase 2: Local Search for Balance Improvement (Reassignment)

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

    #Improvement by reassignment
    for job_id in range(1,n_jobs+1):
        for op_idx in range(len(schedule[job_id])):

            original_machine = schedule[job_id][op_idx]['Assigned Machine']

            machines = jobs[job_id][op_idx][0]

            for new_machine in machines:
                if new_machine != original_machine:
                    temp_schedule = {job_id: [op.copy() for op in schedule[job_id]] for job_id in range(1, n_jobs + 1)}
                    temp_schedule[job_id][op_idx]['Assigned Machine'] = new_machine

                    processing_time = jobs[job_id][op_idx][1][machines.index(new_machine)]
                    temp_schedule[job_id][op_idx]['Processing Time'] = processing_time

                    # Recalculate start and end times for impacted jobs and operations.
                    temp_machine_available_time = {m: 0 for m in range(n_machines)}
                    temp_job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

                    # Rebuild the schedule based on the new machine assignments.
                    is_feasible = True
                    for job_re_id in range(1, n_jobs + 1):
                        # Rebuild schedule.
                        last_end_time = 0
                        for op_re_idx in range(len(schedule[job_re_id])):
                            if job_re_id == job_id and op_re_idx == op_idx:
                                machine = new_machine
                                processing_time = jobs[job_re_id][op_re_idx][1][machines.index(new_machine)]
                            else:
                                machine = schedule[job_re_id][op_re_idx]['Assigned Machine']
                                processing_time = schedule[job_re_id][op_re_idx]['Processing Time']
                            start_time = max(temp_machine_available_time[machine],last_end_time)
                            end_time = start_time + processing_time

                            temp_schedule[job_re_id][op_re_idx]['Start Time'] = start_time
                            temp_schedule[job_re_id][op_re_idx]['End Time'] = end_time

                            temp_machine_available_time[machine] = end_time
                            last_end_time = end_time

                    new_objectives = objective_functions(temp_schedule)

                    if new_objectives['Balance'] < best_objectives['Balance']:
                        best_schedule = {job_id: [op.copy() for op in temp_schedule[job_id]] for job_id in range(1, n_jobs + 1)}
                        best_objectives = new_objectives
                        schedule = {job_id: [op.copy() for op in temp_schedule[job_id]] for job_id in range(1, n_jobs + 1)}

    return best_schedule
