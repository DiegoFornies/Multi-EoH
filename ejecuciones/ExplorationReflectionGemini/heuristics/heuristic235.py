
def heuristic(input_data):
    """Schedules jobs by iterative shortest machine load and earliest job completion."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    unassigned_operations = []
    for job_id, operations in jobs.items():
        for op_idx in range(len(operations)):
            unassigned_operations.append((job_id, op_idx))

    while unassigned_operations:
        best_op = None
        min_end_time = float('inf')

        for job_id, op_idx in unassigned_operations:
            machines, times = jobs[job_id][op_idx]
            for m_idx, machine in enumerate(machines):
                start_time = max(machine_load[machine], job_completion[job_id])
                end_time = start_time + times[m_idx]
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_op = (job_id, op_idx, machine, times[m_idx], start_time)

        job_id, op_idx, machine, time, start_time = best_op
        end_time = start_time + time
        op_num = op_idx + 1

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': time
        })

        machine_load[machine] = end_time
        job_completion[job_id] = end_time
        unassigned_operations.remove((job_id, op_idx))

    return schedule
