
def heuristic(input_data):
    """Schedules jobs minimizing makespan and balancing workload."""
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

        for job_id, op_index in ready_operations:
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

        # Select machine with shortest processing time AND least workload.
        best_machine, best_processing_time = None, float('inf')
        min_combined_score = float('inf')

        load_values = list(machine_workload.values())
        if load_values:
            load_variance = sum([(x - sum(load_values) / len(load_values)) ** 2 for x in load_values]) / (len(load_values)+1e-6)
            delay_factor = 0.01 * load_variance
        else:
            delay_factor = 0.01

        current_makespan = max(machine_available_times.values()) if machine_available_times else 0

        for m_idx, machine_id in enumerate(machines):
            processing_time = times[m_idx]
            available_time = machine_available_times[machine_id]
            start_time = max(available_time, job_completion_times[job_id])
            end_time = start_time + processing_time
            
            #Combined both workload and makespan aware delays
            load_penalty = (machine_workload[machine_id] / (sum(machine_workload.values()) + 1e-6)) * 5
            makespan_delay = (end_time / (current_makespan + 1e-6)) * 5
            combined_delay = load_penalty + makespan_delay

            combined_score = end_time + combined_delay + machine_workload[machine_id] * delay_factor #Incorporating variance

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
