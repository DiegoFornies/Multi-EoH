
def heuristic(input_data):
    """Combines SPT, machine load, and local search for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job_id: [] for job_id in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    eligible_operations = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            eligible_operations.append((job_id, op_idx, machines, times))

    scheduled_operations = set()

    while len(scheduled_operations) < sum(len(ops) for ops in jobs.values()):
        best_operation = None
        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        for job_id, op_idx, machines, times in eligible_operations:
            if (job_id, op_idx) in scheduled_operations:
                continue

            preceding_operations_scheduled = all((job_id, prev_op_idx) in scheduled_operations for prev_op_idx in range(op_idx))
            if not preceding_operations_scheduled:
                continue

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time + processing_time < best_start_time + best_processing_time if best_processing_time else float('inf'):
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
                    best_operation = (job_id, op_idx, machines, times)

        if best_operation:
            job_id, op_idx, machines, times = best_operation
            end_time = best_start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            scheduled_operations.add((job_id, op_idx))

    def calculate_machine_load(current_schedule):
        machine_load_calc = {m: 0 for m in range(n_machines)}
        for job_id in current_schedule:
            for operation in current_schedule[job_id]:
                machine_load_calc[operation['Assigned Machine']] += operation['Processing Time']
        return machine_load_calc

    def calculate_makespan(current_schedule):
        makespan = 0
        for job_id in current_schedule:
            if schedule[job_id]:
                makespan = max(makespan, schedule[job_id][-1]['End Time'])
        return makespan

    def objective_functions(current_schedule):
        machine_load_obj = calculate_machine_load(current_schedule)
        makespan = calculate_makespan(current_schedule)
        total_load = sum(machine_load_obj.values())
        n_machines_used = len([m for m in machine_load_obj if machine_load_obj[m] > 0])
        if n_machines_used > 0:
            balance = sum([(machine_load_obj[m] - (total_load / n_machines_used)) ** 2 for m in machine_load_obj if machine_load_obj[m] > 0]) / n_machines_used
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
                    temp_schedule = {job_id: [op.copy() for op in schedule[job_id]] for job_id in schedule}
                    temp_schedule[job_id][op_idx]['Assigned Machine'] = new_machine
                    processing_time = jobs[job_id][op_idx][1][machines.index(new_machine)]
                    temp_schedule[job_id][op_idx]['Processing Time'] = processing_time

                    temp_machine_available_time = {m: 0 for m in range(n_machines)}
                    temp_job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

                    new_schedule = {}
                    for job_id_re in range(1, n_jobs + 1):
                        new_schedule[job_id_re] = []
                        for op_idx_re in range(len(jobs[job_id_re])):

                            assigned_machine = temp_schedule[job_id_re][op_idx_re]['Assigned Machine'] if job_id_re in temp_schedule and op_idx_re < len(temp_schedule[job_id_re]) else schedule[job_id_re][op_idx_re]['Assigned Machine'] if job_id_re in schedule and op_idx_re < len(schedule[job_id_re]) else machines[0]
                            processing_time_re = next((time for i, time in enumerate(jobs[job_id_re][op_idx_re][1]) if jobs[job_id_re][op_idx_re][0][i] == assigned_machine),0) if job_id_re in jobs and op_idx_re < len(jobs[job_id_re]) else 0

                            start_time = max(temp_machine_available_time[assigned_machine], temp_job_completion_time[job_id_re])
                            end_time = start_time + processing_time_re

                            new_schedule[job_id_re].append({
                                'Operation': op_idx_re + 1,
                                'Assigned Machine': assigned_machine,
                                'Start Time': start_time,
                                'End Time': end_time,
                                'Processing Time': processing_time_re
                            })
                            temp_machine_available_time[assigned_machine] = end_time
                            temp_job_completion_time[job_id_re] = end_time

                    new_objectives = objective_functions(new_schedule)

                    if new_objectives['Makespan'] < best_objectives['Makespan']:
                        best_schedule = new_schedule
                        best_objectives = new_objectives
                        schedule = new_schedule
                    elif new_objectives['Balance'] < best_objectives['Balance'] and new_objectives['Makespan'] == best_objectives['Makespan']:
                        best_schedule = new_schedule
                        best_objectives = new_objectives
                        schedule = new_schedule

    return best_schedule
