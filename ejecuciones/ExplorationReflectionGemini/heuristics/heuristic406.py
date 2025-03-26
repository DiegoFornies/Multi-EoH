
def heuristic(input_data):
    """Combines SPT and earliest start time for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_operations_scheduled = {job: 0 for job in jobs}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        available_operations = []
        for job in jobs:
            op_idx = job_operations_scheduled[job]
            if op_idx < len(jobs[job]):
                available_operations.append({'job': job, 'op_idx': op_idx})

        best_op = None
        best_start_time = float('inf')
        best_processing_time = float('inf')
        best_machine = None
        best_time = None

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                processing_time = time
                if start_time < best_start_time or (start_time == best_start_time and processing_time < best_processing_time):
                    best_start_time = start_time
                    best_processing_time = processing_time
                    best_op = op_data
                    best_machine = machine
                    best_time = time

        if best_op is not None:
            job_id = best_op['job']
            op_idx = best_op['op_idx']
            op_num = op_idx + 1

            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + best_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time
            job_operations_scheduled[job_id] += 1

    return schedule
