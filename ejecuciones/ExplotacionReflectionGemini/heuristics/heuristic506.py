
def heuristic(input_data):
    """Combines greedy scheduling with local search for balance."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    eligible_operations = []
    for job_id in range(1, n_jobs + 1):
        eligible_operations.append((job_id, 0))

    while eligible_operations:
        best_operation = None
        best_machine = None
        earliest_end_time = float('inf')

        for job_id, op_idx in eligible_operations:
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
        eligible_operations.remove((job_id, op_idx))

        if op_idx + 1 < len(jobs[job_id]):
            eligible_operations.append((job_id, op_idx + 1))

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

    for job_id in range(1, n_jobs + 1):
        for op_idx in range(len(schedule[job_id])):
            original_machine = schedule[job_id][op_idx]['Assigned Machine']
            machines = jobs[job_id][op_idx][0]

            for new_machine in machines:
                if new_machine != original_machine:
                    processing_time = jobs[job_id][op_idx][1][machines.index(new_machine)]
                    temp_schedule = {job_id: [op.copy() for op in schedule[job_id]]}
                    temp_schedule[job_id][op_idx]['Assigned Machine'] = new_machine
                    temp_schedule[job_id][op_idx]['Processing Time'] = processing_time

                    temp_machine_available_time = {m: 0 for m in range(n_machines)}
                    temp_job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

                    new_schedule = {}
                    feasible = True
                    for job_id_re in range(1, n_jobs + 1):
                        new_schedule[job_id_re] = []
                        op_completion_time = 0
                        for op_idx_re in range(len(jobs[job_id_re])):

                            # Find best machine based on the original strategy, not the given schedule, for more diversity in local search
                            local_best_machine = None
                            local_earliest_end_time = float('inf')
                            local_processing_time = None

                            machines_local, times_local = jobs[job_id_re][op_idx_re] # possible machines and processing times

                            for machine_idx, machine_local in enumerate(machines_local):

                                processing_time_local = times_local[machine_idx]
                                start_time_local = max(temp_machine_available_time[machine_local], op_completion_time)
                                end_time_local = start_time_local + processing_time_local

                                if end_time_local < local_earliest_end_time: # criteria is Earliest end time.
                                    local_earliest_end_time = end_time_local
                                    local_best_machine = machine_local
                                    local_processing_time = processing_time_local

                            machine = local_best_machine
                            processing_time = local_processing_time

                            start_time = max(temp_machine_available_time[machine], op_completion_time)

                            end_time = start_time + processing_time
                            new_schedule[job_id_re].append({
                                'Operation': op_idx_re + 1,
                                'Assigned Machine': machine,
                                'Start Time': start_time,
                                'End Time': end_time,
                                'Processing Time': processing_time
                            })
                            temp_machine_available_time[machine] = end_time
                            op_completion_time = end_time
                        temp_job_completion_time[job_id_re] = op_completion_time

                    new_objectives = objective_functions(new_schedule)

                    if new_objectives['Balance'] < best_objectives['Balance'] and feasible:
                        best_schedule = new_schedule
                        best_objectives = new_objectives
                        schedule = new_schedule

    return best_schedule
