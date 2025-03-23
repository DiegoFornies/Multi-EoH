
def heuristic(input_data):
    """Schedules jobs minimizing makespan, separation, and balancing workload.
       Uses dynamic weights and lookahead to select operations."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_workload = {m: 0 for m in range(n_machines)}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    makespan_weight = 0.6
    balance_weight = 0.3
    separation_weight = 0.1
    
    while ready_operations:
        best_job, best_op_index = None, None
        best_machine = None
        best_start_time = float('inf')
        min_combined_score = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            for m_idx, machine_id in enumerate(machines):
                processing_time = times[m_idx]
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                end_time = start_time + processing_time
                
                # Makespan component
                makespan_contribution = end_time

                # Balance component
                workload_penalty = machine_workload[machine_id]
                
                #separation Component: add small penalty for job start time overlap
                separation_penalty = 0
                for job in range(1,n_jobs + 1):
                    if job != job_id:
                        if schedule[job]:
                            prev_job_end_time = schedule[job][-1]['End Time']
                            separation_penalty += max(0, 1 - (start_time - prev_job_end_time))
                #Calculate Combined score
                combined_score = (makespan_weight * makespan_contribution +
                                  balance_weight * workload_penalty +
                                  separation_weight * separation_penalty)

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_job = job_id
                    best_op_index = op_index
                    best_machine = machine_id
                    best_start_time = start_time
                    best_processing_time = processing_time

        # Schedule the best operation
        job_id = best_job
        op_index = best_op_index
        best_machine = best_machine
        best_processing_time = best_processing_time
        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time
        
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_workload[best_machine] += best_processing_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        ready_operations.remove((job_id, op_index))

        if op_index + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_index + 1))

        # Dynamic Weight Adjustment
        makespan_weight = 0.6
        balance_weight = 0.3
        separation_weight = 0.1

    return schedule
