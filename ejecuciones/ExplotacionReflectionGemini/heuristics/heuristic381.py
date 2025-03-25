
def heuristic(input_data):
    """Combines greedy scheduling with load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    remaining_operations = {j: len(jobs[j]) for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, op_data))

    scheduled_operations = set()

    while any(remaining_operations[job] > 0 for job in range(1, n_jobs + 1)):
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
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
        min_score = float('inf')

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data
            remaining = remaining_operations[job_id]

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                # Score considers remaining ops, idle time, & machine load.
                score = remaining + start_time + 0.5 * machine_load[machine]

                if score < min_score:
                    min_score = score
                    best_operation = (job_id, op_idx, machine, start_time, processing_time)

        if best_operation:
            job_id, op_idx, machine, start_time, processing_time = best_operation
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
            remaining_operations[job_id] -= 1
            scheduled_operations.add((job_id, op_idx))
            machine_load[machine] += processing_time
        else:
            break
            
    # Load balance by machine reassignment
    def calculate_machine_load(current_schedule):
        machine_load = {m: 0 for m in range(n_machines)}
        for job_id in current_schedule:
            for operation in current_schedule[job_id]:
                machine_load[operation['Assigned Machine']] += operation['Processing Time']
        return machine_load

    def calculate_makespan(current_schedule):
        makespan = 0
        for job_id in current_schedule:
            if current_schedule[job_id]:
                makespan = max(makespan, current_schedule[job_id][-1]['End Time'])
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

    best_schedule = {k: [op.copy() for op in v] for k, v in schedule.items()}
    best_objectives = objective_functions(best_schedule)

    # Machine Reassignment to improve load balance
    for job_id in range(1, n_jobs + 1):
        for op_idx in range(len(schedule[job_id])):
            original_machine = schedule[job_id][op_idx]['Assigned Machine']
            machines = jobs[job_id][op_idx][0]

            for new_machine in machines:
                if new_machine != original_machine:
                    temp_schedule = {k: [op.copy() for op in v] for k, v in schedule.items()}

                    # Correctly assign the new machine
                    temp_schedule[job_id][op_idx]['Assigned Machine'] = new_machine

                    # Get processing time from correct machine
                    processing_time = jobs[job_id][op_idx][1][machines.index(new_machine)]
                    temp_schedule[job_id][op_idx]['Processing Time'] = processing_time

                    # Recalculate start and end times based on updated machine assignments
                    temp_machine_available_time = {m: 0 for m in range(n_machines)}
                    temp_job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

                    is_feasible = True  # Flag for feasibility

                    # Reschedule affected operations after reassignment
                    reschedule_start_job = job_id
                    reschedule_start_op = op_idx

                    # Recalculate schedule based on machine reassignment
                    recalculated_schedule = {job_id_re: [] for job_id_re in range(1, n_jobs + 1)}

                    # Build the new schedule
                    for job_id_re in range(1, n_jobs + 1):
                        for op_idx_re in range(len(temp_schedule[job_id_re])):
                            machine_to_use = temp_schedule[job_id_re][op_idx_re]['Assigned Machine']
                            processing_time = temp_schedule[job_id_re][op_idx_re]['Processing Time']
                            start_time = max(temp_machine_available_time[machine_to_use], temp_job_completion_time[job_id_re])
                            end_time = start_time + processing_time

                            recalculated_schedule[job_id_re].append({
                                'Operation': op_idx_re + 1,
                                'Assigned Machine': machine_to_use,
                                'Start Time': start_time,
                                'End Time': end_time,
                                'Processing Time': processing_time
                            })

                            temp_machine_available_time[machine_to_use] = end_time
                            temp_job_completion_time[job_id_re] = end_time

                    if is_feasible:
                        new_objectives = objective_functions(recalculated_schedule)
                        if new_objectives['Balance'] < best_objectives['Balance']:
                            best_schedule = {k: [op.copy() for op in v] for k, v in recalculated_schedule.items()}
                            best_objectives = new_objectives
                            schedule = recalculated_schedule

    return best_schedule
