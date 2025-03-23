
def heuristic(input_data):
    """Schedules jobs considering makespan, machine workload, and job wait times."""
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
        min_combined_score = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            for m_idx, machine_id in enumerate(machines):
                processing_time = times[m_idx]
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                end_time = start_time + processing_time

                # Calculate workload imbalance penalty
                avg_workload = sum(machine_workload.values()) / n_machines if n_machines > 0 else 0
                workload_diff = machine_workload[machine_id] - avg_workload
                workload_penalty = max(0, workload_diff)  # Only penalize machines above average
                
                # Calculate job waiting time penalty
                wait_time = start_time - job_completion_times[job_id] if job_id in job_completion_times else start_time
                wait_time_penalty = max(0, wait_time) # Penaltize jobs that wait for machine

                # Combine factors, weighting makespan reduction higher
                combined_score = end_time + 0.5 * workload_penalty + 0.3 * wait_time_penalty  # Adjust weights as needed

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_job, best_op_index = job_id, op_index
                    best_machine = machine_id
                    best_processing_time = processing_time
                    best_start_time = start_time

        job_id, op_index = best_job, best_op_index

        machines, times = jobs_data[job_id][op_index]

        best_processing_time = next(time for m_idx, time in enumerate(times) if machines[m_idx] == best_machine)

        start_time = max(machine_available_times[best_machine], job_completion_times[job_id] if job_id in job_completion_times else 0)
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
