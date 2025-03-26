
def heuristic(input_data):
    """Schedules jobs using a hybrid approach: earliest start time & balanced machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        best_op = None
        best_start_time = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            earliest_start_time = float('inf')
            selected_machine = None
            selected_time = None

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                
                #consider machine load and earliest available time
                weighted_time = start_time + (machine_load[machine] / (sum(machine_load.values()) + 1e-6) if sum(machine_load.values()) > 0 else 0) * time
                
                if weighted_time < earliest_start_time:
                    earliest_start_time = weighted_time
                    selected_machine = machine
                    selected_time = time

            if selected_machine is not None:
                job_id = op_data['job']
                op_idx = op_data['op_idx']
                op_num = op_idx + 1

                start_time = max(machine_available_times[selected_machine], job_completion_times[job_id])
                end_time = start_time + selected_time

                schedule[job_id].append({
                    'Operation': op_num,
                    'Assigned Machine': selected_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': selected_time
                })

                machine_available_times[selected_machine] = end_time
                machine_load[selected_machine] += selected_time
                job_completion_times[job_id] = end_time

                available_operations.remove(op_data)
                if op_idx + 1 < len(jobs[job_id]):
                    available_operations.append({'job': job_id, 'op_idx': op_idx + 1})
            else:
                available_operations.remove(op_data)


    return schedule
