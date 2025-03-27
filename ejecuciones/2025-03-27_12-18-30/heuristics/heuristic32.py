
def heuristic(input_data):
    """Combines SPT with machine availability for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    operation_queue = []
    for job, ops in jobs.items():
        operation_queue.append((job, 0))

    while operation_queue:
        best_job, best_op_idx = None, None
        min_end_time = float('inf')

        for job, op_idx in operation_queue:
            machines, times = jobs[job][op_idx]

            for i, machine in enumerate(machines):
                start_time = max(machine_time[machine], job_completion_time[job])
                end_time = start_time + times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_job, best_op_idx = job, op_idx
                    best_machine = machine
                    best_processing_time = times[i]
                    best_start_time = start_time

        job = best_job
        op_idx = best_op_idx
        operation_queue.remove((job, op_idx))
        op_num = op_idx + 1

        start = best_start_time
        end = start + best_processing_time
        m = best_machine

        if job not in schedule:
            schedule[job] = []
        schedule[job].append({'Operation': op_num, 'Assigned Machine': m, 'Start Time': start, 'End Time': end, 'Processing Time': best_processing_time})

        machine_time[m] = end
        job_completion_time[job] = end

        if op_idx + 1 < len(jobs[job]):
            operation_queue.append((job, op_idx + 1))

    return schedule
