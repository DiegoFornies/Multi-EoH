
def heuristic(input_data):
    """Schedules jobs minimizing makespan, balancing workload, and separation by considering machine idle times."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_workload = {m: 0 for m in range(n_machines)}
    machine_idle_times = {m: [] for m in range(n_machines)} # Track idle times for separation

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        best_machine = None
        earliest_end_time = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            for m_idx, machine_id in enumerate(machines):
                processing_time = times[m_idx]
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                end_time = start_time + processing_time
                idle_time_penalty = 0
                
                # Separation factor: Incentivize use of machines that have been idle longer, penalize short idle times
                idle_durations = [end - start for start, end in machine_idle_times[machine_id] if end <= start_time]
                if idle_durations:
                    idle_time_penalty = -sum(idle_durations)

                # Workload balance
                load_penalty = (machine_workload[machine_id] / (sum(machine_workload.values()) + 1e-6)) * 5

                # Heuristic weight configuration
                makespan_weight = 1.0
                load_weight = 1.5
                separation_weight = 0.1
                
                # Combined score with heuristic weights
                combined_score = makespan_weight * end_time + load_weight * load_penalty + separation_weight * idle_time_penalty

                if combined_score < earliest_end_time:
                    earliest_end_time = combined_score
                    best_job = job_id
                    best_op_index = op_index
                    best_machine = machine_id
                    best_processing_time = processing_time
                    best_start_time = start_time


        job_id, op_index = best_job, best_op_index
        best_machine = best_machine
        best_processing_time = best_processing_time
        start_time = best_start_time

        end_time = start_time + best_processing_time
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_workload[best_machine] += best_processing_time

        # Update idle times
        machine_idle_times[best_machine].append((machine_available_times[best_machine] - best_processing_time, machine_available_times[best_machine]))
        machine_idle_times[best_machine].sort()

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
