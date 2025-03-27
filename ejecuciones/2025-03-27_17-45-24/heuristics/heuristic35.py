
def heuristic(input_data):
    """Schedule jobs minimizing makespan and balancing load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    # Prioritize jobs with more remaining operations
    job_priority = {j: len(jobs_data[j]) for j in range(1, n_jobs + 1)}

    scheduled_operations = 0
    total_operations = sum(len(ops) for ops in jobs_data.values())

    while scheduled_operations < total_operations:
        eligible_jobs = [j for j in range(1, n_jobs + 1) if job_priority[j] > 0]

        if not eligible_jobs:
            break

        # Select job based on priority (remaining operations)
        selected_job = max(eligible_jobs, key=lambda j: job_priority[j])
        op_index = len(schedule[selected_job])
        machines, times = jobs_data[selected_job][op_index]

        # Choose machine based on earliest finish time and machine load
        best_machine = None
        min_finish_time = float('inf')

        for m_index, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[selected_job])
            finish_time = start_time + times[m_index]
            load_factor = machine_load[machine] # Load to avoid machine selection
            
            if finish_time + load_factor < min_finish_time:
                min_finish_time = finish_time + load_factor
                best_machine = machine
                best_start_time = start_time
                best_processing_time = times[m_index]

        if best_machine is not None:
            schedule[selected_job].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[selected_job] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_priority[selected_job] -= 1
            scheduled_operations += 1

    return schedule
