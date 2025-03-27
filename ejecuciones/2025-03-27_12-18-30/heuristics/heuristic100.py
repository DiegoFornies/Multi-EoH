
def heuristic(input_data):
    """Combines SPT and load balancing with dynamic weight."""
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
        best_score = float('inf')

        for job, op_idx in operation_queue:
            machines, times = jobs[job][op_idx]
            
            for i, m in enumerate(machines):
                start_time = max(machine_time[m], job_completion_time[job])
                processing_time = times[i]

                # Dynamic weight based on machine load and job urgency
                machine_load_factor = machine_time[m] / (sum(machine_time.values()) / n_machines + 1e-9)
                job_urgency_factor = job_completion_time[job] / (sum(job_completion_time.values()) / n_jobs + 1e-9)
                
                # Adjusted score considering makespan impact, load balancing, and job urgency
                score = (start_time + processing_time) * (0.6 + 0.2 * machine_load_factor) + 0.2 * job_urgency_factor
                                
                if score < best_score:
                    best_score = score
                    best_job, best_op_idx = job, op_idx
                    best_machine = m
                    best_start_time = start_time
                    best_processing_time = processing_time
                    
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
