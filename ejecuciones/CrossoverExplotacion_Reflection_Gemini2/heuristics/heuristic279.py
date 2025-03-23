
def heuristic(input_data):
    """Schedules jobs minimizing makespan and improving separation."""
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
        earliest_start_time = float('inf')

        # Prioritize jobs with more remaining operations or shorter overall duration to
        # reduce makespan and improve flow.
        job_priorities = {}
        for job_id, op_index in ready_operations:
            remaining_operations = len(jobs_data[job_id]) - op_index
            total_processing_time = 0
            for future_op_index in range(op_index, len(jobs_data[job_id])):
              machines, times = jobs_data[job_id][future_op_index]
              total_processing_time += min(times) # Assuming shortest processing time possible

            job_priorities[job_id, op_index] = (remaining_operations, -total_processing_time) #Prioritize more operations, shorter time

        sorted_ready_operations = sorted(ready_operations, key=lambda x: job_priorities[x[0], x[1]], reverse=True)

        for job_id, op_index in sorted_ready_operations:
            machines, times = jobs_data[job_id][op_index]

            min_start_time = float('inf')
            for machine_id, processing_time in zip(machines, times):
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                min_start_time = min(min_start_time, start_time)

            if min_start_time < earliest_start_time:
                earliest_start_time = min_start_time
                best_job, best_op_index = job_id, op_index

        job_id, op_index = best_job, best_op_index
        machines, times = jobs_data[job_id][op_index]

        # Select machine balancing makespan and workload while increasing separation
        best_machine, best_processing_time = None, float('inf')
        min_combined_score = float('inf')

        current_makespan = max(machine_available_times.values()) if machine_available_times else 0

        #Improved separation strategy: penalize machine selections that place operations from the same job close together.
        job_history = [op['Assigned Machine'] for op in schedule[job_id] if schedule[job_id]]
        separation_penalty = 0

        for m_idx, machine_id in enumerate(machines):
            processing_time = times[m_idx]
            available_time = machine_available_times[machine_id]
            start_time = max(available_time, job_completion_times[job_id])
            end_time = start_time + processing_time

            #Penalty if the machine was previously used by this job recently
            if job_history and job_history[-1] == machine_id:
              separation_penalty = 10 #Tuning this matters!
            else:
              separation_penalty = 0

            # Load balancing penalty based on relative workload, scaled to processing time
            workload_ratio = machine_workload[machine_id] / (sum(machine_workload.values()) + 1e-6) if sum(machine_workload.values()) > 0 else 0
            load_penalty = workload_ratio * processing_time * 2  # Scale penalty by processing time

            makespan_delay = (end_time / (current_makespan + 1e-6)) * 1 #Smaller impact on makespan, focus balance

            combined_score = end_time + load_penalty + makespan_delay + separation_penalty
            
            if combined_score < min_combined_score:
                min_combined_score = combined_score
                best_machine = machine_id
                best_processing_time = processing_time
                best_start_time = start_time

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
