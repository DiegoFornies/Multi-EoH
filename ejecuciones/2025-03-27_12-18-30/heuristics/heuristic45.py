
def heuristic(input_data):
    """Earliest Due Date (EDD) with machine consideration."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_due_date = {} # Simulate a due date (total processing time)

    for job, ops in jobs.items():
        total_time = 0
        for machines, times in ops:
            total_time += min(times) # Assume best case processing time
        job_due_date[job] = total_time

    operation_queue = []
    for job, ops in jobs.items():
        operation_queue.append((job, 0))

    while operation_queue:
        best_job, best_op_idx = None, None
        min_due_date = float('inf')

        for job, op_idx in operation_queue:
            if job_due_date[job] < min_due_date:
                min_due_date = job_due_date[job]
                best_job, best_op_idx = job, op_idx

        job = best_job
        op_idx = best_op_idx
        operation_queue.remove((job, op_idx))

        machines, times = jobs[job][op_idx]
        op_num = op_idx + 1

        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for i, m in enumerate(machines):
            start_time = max(machine_time[m], (schedule[job][-1]['End Time'] if job in schedule and schedule[job] else 0 )) # Sequence feasibility!
            processing_time = times[i]

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = m
                best_processing_time = processing_time

        start = best_start_time
        end = start + best_processing_time
        m = best_machine

        if job not in schedule:
            schedule[job] = []
        schedule[job].append({'Operation': op_num, 'Assigned Machine': m, 'Start Time': start, 'End Time': end, 'Processing Time': best_processing_time})

        machine_time[m] = end

        if op_idx + 1 < len(jobs[job]):
            operation_queue.append((job, op_idx + 1))

    return schedule
