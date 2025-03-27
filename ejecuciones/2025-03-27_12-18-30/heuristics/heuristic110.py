
def heuristic(input_data):
    """Combines SPT, EDD, and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_due_dates = {}  # Assuming equal to the sum of processing times
    for job in jobs:
        due_date = 0
        for machines, times in jobs[job]:
            due_date += min(times)
        job_due_dates[job] = due_date

    operation_queue = []
    for job, ops in jobs.items():
        operation_queue.append((job, 0))

    while operation_queue:
        best_job, best_op_idx = None, None
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        best_priority = float('inf')

        for job, op_idx in operation_queue:
            machines, times = jobs[job][op_idx]

            for i, m in enumerate(machines):
                start_time = max(machine_time[m], job_completion_time[job])
                processing_time = times[i]
                end_time = start_time + processing_time

                # SPT + EDD + Load Balancing
                # SPT: processing_time
                # EDD: job_due_dates[job] - end_time
                # Load balancing: machine_time[m] + processing_time

                priority = (0.4 * processing_time + 0.3 * max(0, job_due_dates[job] - end_time) + 0.3 * (machine_time[m] + processing_time))  # Prioritize smaller processing times, early due dates, and less loaded machine

                if priority < best_priority:
                    best_priority = priority
                    best_job, best_op_idx = job, op_idx
                    best_machine, best_start_time, best_processing_time = m, start_time, processing_time
        
        job = best_job
        op_idx = best_op_idx
        operation_queue.remove((job, op_idx))
        m = best_machine
        start = best_start_time
        processing_time = best_processing_time
        end = start + processing_time
        op_num = op_idx + 1


        if job not in schedule:
            schedule[job] = []
        schedule[job].append({'Operation': op_num, 'Assigned Machine': m, 'Start Time': start, 'End Time': end, 'Processing Time': processing_time})

        machine_time[m] = end
        job_completion_time[job] = end

        if op_idx + 1 < len(jobs[job]):
            operation_queue.append((job, op_idx + 1))

    return schedule
