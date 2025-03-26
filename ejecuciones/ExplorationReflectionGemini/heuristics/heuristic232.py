
def heuristic(input_data):
    """Schedules jobs balancing load and minimizing makespan."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        best_op = None
        best_start_time = float('inf')
        best_processing_time = float('inf')
        best_machine = None

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_time[machine], job_completion_time[job_id])
                processing_time = time
                machine_load = processing_time / (machine_time[machine] + 1e-6)
                priority = start_time + machine_load  # Combine earliest start and load

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_processing_time = time
                    best_machine = machine
                    best_op = op_data
                elif start_time == best_start_time and processing_time < best_processing_time:
                     best_processing_time = time
                     best_machine = machine
                     best_op = op_data

        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        start_time = max(machine_time[best_machine], job_completion_time[job_id])
        processing_time = jobs[job_id][op_idx][1][jobs[job_id][op_idx][0].index(best_machine)]

        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
