
def heuristic(input_data):
    """Combines SPT, least load, and operation-centric view."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append({'job': job_id, 'op_idx': 0})
        schedule[job_id] = []

    while available_operations:
        best_op = None
        best_score = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            best_machine = None
            best_time = float('inf')
            earliest_start_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    best_time = time
            
            machine_load = machine_available_times[best_machine]
            score = 0.7 * (earliest_start_time + best_time) + 0.3 * machine_load
            
            if score < best_score:
                best_score = score
                best_op = op_data
                selected_machine = best_machine
                selected_time = best_time
                start_time_select = earliest_start_time

        job_id = best_op['job']
        op_idx = best_op['op_idx']

        start_time = max(machine_available_times[selected_machine], job_completion_times[job_id])
        end_time = start_time + selected_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': selected_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': selected_time
        })

        machine_available_times[selected_machine] = end_time
        job_completion_times[job_id] = end_time

        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
