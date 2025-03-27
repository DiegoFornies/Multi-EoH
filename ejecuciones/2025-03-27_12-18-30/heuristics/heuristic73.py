
def heuristic(input_data):
    """Combines EDD and SPT with machine load to balance makespan."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    job_due_dates = {}
    for job in range(1, n_jobs + 1):
        total_processing_time = 0
        for machines, times in jobs[job]:
            total_processing_time += min(times)
        job_due_dates[job] = total_processing_time

    job_order = sorted(job_due_dates.items(), key=lambda item: item[1])

    operation_queue = []
    for job, _ in job_order:
        operation_queue.append((job, 0))

    while operation_queue:
        best_job, best_op_idx = None, None
        min_makespan_impact = float('inf')

        for job, op_idx in operation_queue:
            machines, times = jobs[job][op_idx]
            best_machine_local, best_start_time_local, best_processing_time_local = None, float('inf'), None
            
            for i, m in enumerate(machines):
                start_time = max(machine_time[m], job_completion_time[job])
                processing_time = times[i]

                if start_time < best_start_time_local:
                    best_start_time_local = start_time
                    best_machine_local = m
                    best_processing_time_local = processing_time
                elif start_time == best_start_time_local and machine_time[m] < machine_time[best_machine_local]:
                    best_machine_local = m
                    best_processing_time_local = processing_time
            
            makespan_impact = best_start_time_local + best_processing_time_local
            if makespan_impact < min_makespan_impact:
                min_makespan_impact = makespan_impact
                best_job, best_op_idx = job, op_idx

        job = best_job
        op_idx = best_op_idx
        operation_queue.remove((job, op_idx))

        machines, times = jobs[job][op_idx]
        op_num = op_idx + 1

        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for i, m in enumerate(machines):
            start_time = max(machine_time[m], job_completion_time[job])
            processing_time = times[i]

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = m
                best_processing_time = processing_time
            elif start_time == best_start_time and machine_time[m] < machine_time[best_machine]:
                best_machine = m
                best_processing_time = processing_time

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
