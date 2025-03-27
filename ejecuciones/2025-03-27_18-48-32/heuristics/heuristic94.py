
def heuristic(input_data):
    """A hybrid heuristic combining makespan, load balancing, and separation."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_assignments = {m: [] for m in range(n_machines)}

    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    def calculate_score(job, op_num, machine, start_time, processing_time):
        """Combines makespan, machine load, and separation for scoring."""
        end_time = start_time + processing_time
        machine_load = machine_available_time[machine]

        #Dynamic Weighting
        makespan_weight = 0.6
        load_weight = 0.2
        separation_weight = 0.2

        #Separation score
        separation = 0
        for assigned_job in machine_assignments[machine]:
            if assigned_job != job:
                separation += 1 #Simple penalty for jobs near each other

        score = makespan_weight * end_time + load_weight * machine_load + separation_weight * separation
        return score

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                for m_idx, m in enumerate(machines):
                    start_time = max(machine_available_time[m], job_completion_time[job])
                    eligible_operations.append((job, op_num, m, start_time, times[m_idx]))

        best_operation = None
        best_score = float('inf')

        for job, op_num, machine, start_time, processing_time in eligible_operations:
            score = calculate_score(job, op_num, machine, start_time, processing_time)
            if score < best_score:
                best_score = score
                best_operation = (job, op_num, machine, start_time, processing_time)

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
