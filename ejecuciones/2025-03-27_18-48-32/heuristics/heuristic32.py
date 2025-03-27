
def heuristic(input_data):
    """Heuristic for FJSSP minimizing makespan and machine idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    schedule = {}
    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times, job))

        # Select the operation with the shortest processing time
        best_operation = None
        best_makespan = float('inf')

        for op_num, machines, times, job in [(op[1], op[2], op[3], op[4]) for op in eligible_operations]:
            job_id = job
            possible_makespans = []
            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_time[m], job_completion_time[job_id])
                end_time = start_time + times[m_idx]
                possible_makespans.append((end_time, m, start_time, times[m_idx]))

            min_end_time = min(possible_makespans, key=lambda x: (x[0]))

            if min_end_time[0] < best_makespan:
                best_makespan = min_end_time[0]
                best_operation = (op_num, min_end_time[1], min_end_time[2], min_end_time[3], job)

        if best_operation:
            op_num, machine, start_time, processing_time, job = best_operation
            job_id = job

            if job_id not in schedule:
                schedule[job_id] = []

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': start_time + processing_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = start_time + processing_time
            job_completion_time[job_id] = start_time + processing_time
            remaining_operations[job_id].pop(0)

    return schedule
