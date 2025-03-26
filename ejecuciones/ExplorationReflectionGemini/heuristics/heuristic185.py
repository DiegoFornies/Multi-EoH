
def heuristic(input_data):
    """Combines SPT job prioritization with adaptive machine selection based on load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    job_processing_times = {}
    for job_id in range(1, n_jobs + 1):
        total_time = 0
        for machines, times in jobs[job_id]:
            total_time += min(times)
        job_processing_times[job_id] = total_time

    job_priority = sorted(range(1, n_jobs + 1), key=lambda x: job_processing_times[x])
    job_operations_scheduled = {job: 0 for job in range(1, n_jobs + 1)}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in range(1, n_jobs + 1)):
        for job_id in job_priority:
            next_op_index = job_operations_scheduled[job_id]
            if next_op_index >= len(jobs[job_id]):
                continue

            machines, times = jobs[job_id][next_op_index]
            operation_number = next_op_index + 1

            best_machine = None
            min_start_time = float('inf')
            processing_time = None

            for i, machine in enumerate(machines):
                start_time = max(machine_load[machine], job_completion_times[job_id])
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    processing_time = times[i]

            if best_machine is not None:
                start_time = max(machine_load[best_machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                schedule[job_id].append({
                    'Operation': operation_number,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })

                machine_load[best_machine] = end_time
                job_completion_times[job_id] = end_time
                job_operations_scheduled[job_id] += 1

    return schedule
