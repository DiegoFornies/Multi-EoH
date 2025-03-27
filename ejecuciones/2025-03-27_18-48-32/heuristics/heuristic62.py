
def heuristic(input_data):
    """
    FJSSP heuristic: Combines makespan & machine load, with tie-breaking
    based on fewer jobs. Balances objectives dynamically.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_assignments = {m: [] for m in range(n_machines)}

    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times))

        # Select the operation with the best score.
        best_operation = None
        best_score = float('inf')
        contenders = []

        for job, op_num, machines, times in eligible_operations:
            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_time[m], job_completion_time[job])
                end_time = start_time + times[m_idx]
                machine_load = machine_available_time[m]

                score = end_time + 0.1 * machine_load

                if score < best_score:
                    best_score = score
                    contenders = [(job, op_num, m, start_time, times[m_idx])]
                elif score == best_score:
                    contenders.append((job, op_num, m, start_time, times[m_idx]))

        #Tie-breaking: Prefer machine with fewer jobs
        if len(contenders) > 1:
            best_machine = min([c[2] for c in contenders], key = lambda m: len(machine_assignments[m]))
            best_operation = next(c for c in contenders if c[2] == best_machine)
        elif len(contenders) == 1:
            best_operation = contenders[0]
        else:
            best_operation = None

        if best_operation:
            job, op_num, machine, start_time, processing_time = best_operation

            if job not in schedule:
                schedule[job] = []

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': start_time + processing_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = start_time + processing_time
            job_completion_time[job] = start_time + processing_time
            machine_assignments[machine].append(job)

            remaining_operations[job].pop(0)

    return schedule
