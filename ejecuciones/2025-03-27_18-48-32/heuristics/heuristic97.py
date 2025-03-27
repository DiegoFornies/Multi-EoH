
def heuristic(input_data):
    """Schedules jobs by shortest processing time, balanced with machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times, job))

        # Prioritize shortest processing time, balance load
        best_operation = None
        best_score = float('inf')

        for op_num, machines, times, job in ((op[1], op[2], op[3], op[4]) for op in eligible_operations):
            job_num = next(op[0] for op in eligible_operations if op[1] == op_num and op[2] == machines and op[3] == times)
            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_time[m], job_completion_time[job_num])
                processing_time = times[m_idx]
                #score = processing_time + machine_available_time[m]
                score = processing_time + 0.1 * machine_available_time[m]
                if score < best_score:
                    best_score = score
                    best_operation = (job_num, op_num, m, start_time, processing_time)

        if best_operation:
            job_num, op_num, machine, start_time, processing_time = best_operation

            if job_num not in schedule:
                schedule[job_num] = []

            schedule[job_num].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': start_time + processing_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = start_time + processing_time
            job_completion_time[job_num] = start_time + processing_time

            remaining_operations[job_num].pop(0)

    return schedule
