
def heuristic(input_data):
    """Prioritizes shortest operation and least loaded machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    remaining_ops = {}
    for job_id, operations in jobs.items():
        remaining_ops[job_id] = list(range(len(operations)))

    while any(remaining_ops.values()):
        best_job, best_op_idx, best_machine, best_start, best_time = None, None, None, float('inf'), None

        for job_id, ops in remaining_ops.items():
            if not ops:
                continue
            op_idx = ops[0]
            machines, times = jobs[job_id][op_idx]

            for i, machine in enumerate(machines):
                start_time = max(machine_load[machine], job_completion[job_id])
                if start_time < best_start:
                    best_start = start_time
                    best_job = job_id
                    best_op_idx = op_idx
                    best_machine = machine
                    best_time = times[i]

        if best_job is None:
            return "Infeasible solution"

        start_time = max(machine_load[best_machine], job_completion[best_job])
        end_time = start_time + best_time
        op_num = best_op_idx + 1

        schedule[best_job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_load[best_machine] = end_time
        job_completion[best_job] = end_time
        remaining_ops[best_job].pop(0)
    return schedule
