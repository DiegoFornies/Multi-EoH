
def heuristic(input_data):
    """Combines SPT, earliest start, and load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    available_ops = []
    for job_id in jobs:
        available_ops.append({'job': job_id, 'op_idx': 0})

    while available_ops:
        best_op, best_machine, best_start = None, None, float('inf')
        best_process_time = float('inf')

        for op in available_ops:
            job_id, op_idx = op['job'], op['op_idx']
            machines, times = jobs[job_id][op_idx]

            earliest_start = float('inf')
            selected_machine, selected_time = None, None

            for i, machine in enumerate(machines):
                start = max(machine_available[machine], job_completion[job_id])
                if start < earliest_start:
                    earliest_start = start
                    selected_machine, selected_time = machine, times[i]
                elif start == earliest_start and times[i] < selected_time:
                  selected_machine, selected_time = machine, times[i]
            
            process_time = selected_time
            if earliest_start < best_start or (earliest_start == best_start and process_time < best_process_time):
                best_start, best_process_time = earliest_start, process_time
                best_op, best_machine, best_time = op, selected_machine, selected_time

        job_id, op_idx = best_op['job'], best_op['op_idx']
        start = max(machine_available[best_machine], job_completion[job_id])
        end = start + best_time
        op_num = op_idx + 1
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start,
            'End Time': end,
            'Processing Time': best_time
        })

        machine_available[best_machine] = end
        job_completion[job_id] = end
        available_ops.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_ops.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
