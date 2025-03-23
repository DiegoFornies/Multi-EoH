
def heuristic(input_data):
    """Schedules jobs minimizing makespan, separation, and balance."""
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

    while ready_operations:
        best_job, best_op_index = None, None
        best_machine = None
        min_combined_score = float('inf')
        
        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            for m_idx, machine_id in enumerate(machines):
                processing_time = times[m_idx]
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                end_time = start_time + processing_time

                # Dynamic Weight Adjustment: Separation and balance
                makespan = max(machine_available_times.values()) if machine_available_times else 0

                # Adjust for Makespan
                makespan_weight = 0.5
                makespan_score = end_time * makespan_weight if makespan > 0 else 0

                # Adjust for Balance
                workload_deviation = sum([(work - sum(machine_workload.values()) / n_machines) ** 2 for work in machine_workload.values()]) / n_machines if n_machines > 0 else 0
                balance_weight = 0.3
                balance_score = (machine_workload[machine_id] + processing_time) * balance_weight * workload_deviation

                #Adjust for Job separation
                separation_weight = 0.2
                separation_score = start_time * separation_weight

                combined_score = makespan_score + balance_score + separation_score

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_job = job_id
                    best_op_index = op_index
                    best_machine = machine_id
                    best_processing_time = processing_time
                    best_start_time = start_time

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

    return schedule
