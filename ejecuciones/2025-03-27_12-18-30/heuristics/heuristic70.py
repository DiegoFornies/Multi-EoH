
def heuristic(input_data):
    """Balances makespan and machine load using adaptive weighting."""
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
        best_machine = None
        min_weighted_score = float('inf')

        for job, op_idx in operation_queue:
            machines, times = jobs[job][op_idx]
            job_operations_count = len(jobs[job])
            for i, m in enumerate(machines):
                start_time = max(machine_time[m], job_completion_time[job])
                processing_time = times[i]
                makespan_impact = start_time + processing_time
                machine_load = machine_time[m]
                
                # Adaptive weighting: SPT and load balancing
                #More number of operations mean more important
                weight_makespan = 0.6
                weight_load = 0.4

                weighted_score = weight_makespan * makespan_impact + weight_load * machine_load
                
                if weighted_score < min_weighted_score:
                    min_weighted_score = weighted_score
                    best_job = job
                    best_op_idx = op_idx
                    best_machine = m
                    best_start_time = start_time
                    best_processing_time = processing_time

        job = best_job
        op_idx = best_op_idx
        operation_queue.remove((job, op_idx))

        start = best_start_time
        end = start + best_processing_time
        m = best_machine
        op_num = op_idx + 1

        if job not in schedule:
            schedule[job] = []
        schedule[job].append({'Operation': op_num, 'Assigned Machine': m, 'Start Time': start, 'End Time': end, 'Processing Time': best_processing_time})

        machine_time[m] = end
        job_completion_time[job] = end

        if op_idx + 1 < len(jobs[job]):
            operation_queue.append((job, op_idx + 1))

    return schedule
