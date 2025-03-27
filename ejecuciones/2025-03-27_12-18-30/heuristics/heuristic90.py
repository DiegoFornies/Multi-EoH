
def heuristic(input_data):
    """
    Adaptive heuristic: SPT + Load Balancing. Balances makespan and load
    based on job complexity (number of operations).
    """
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
        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for job, op_idx in operation_queue:
            machines, times = jobs[job][op_idx]
            op_num = op_idx + 1

            # SPT calculation for current operation
            best_machine_local, best_start_time_local, best_processing_time_local = None, float('inf'), None
            for i, m in enumerate(machines):
                start_time = max(machine_time[m], job_completion_time[job])
                processing_time = times[i]

                if start_time < best_start_time_local:
                    best_start_time_local = start_time
                    best_machine_local = m
                    best_processing_time_local = processing_time

            #Load Balancing factor, favor machine with early available time
            load_balance_factor = 0.1 * (len(jobs[job])) # Weight based on job complexity (operations num)
            makespan_impact = best_start_time_local + best_processing_time_local + load_balance_factor*machine_time[best_machine_local]

            if makespan_impact < best_start_time:
                best_job, best_op_idx = job, op_idx
                best_machine = best_machine_local
                best_start_time = best_start_time_local
                best_processing_time = best_processing_time_local

        job = best_job
        op_idx = best_op_idx
        operation_queue.remove((job, op_idx))

        machines, times = jobs[job][op_idx]
        op_num = op_idx + 1
        best_processing_time = best_processing_time
        best_start_time = best_start_time
        best_machine= best_machine
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
