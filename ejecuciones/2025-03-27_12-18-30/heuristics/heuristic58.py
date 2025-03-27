
def heuristic(input_data):
    """FJSSP heuristic: Combines SPT, least loaded machine, and dynamic job re-prioritization."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_queue = list(range(1, n_jobs + 1))
    job_operation_index = {job: 0 for job in range(1, n_jobs + 1)}

    while job_queue:
        job = job_queue.pop(0)  # Prioritized Job
        op_idx = job_operation_index[job]

        if op_idx >= len(jobs[job]):
            continue # Job finished

        machines, times = jobs[job][op_idx]
        
        eligible_machines = []
        for m_idx, m in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[m], (schedule[job][-1]['End Time'] if schedule[job] else 0) if op_idx>0 else 0)
            eligible_machines.append((m, start_time, processing_time))

        if not eligible_machines:
            job_queue.append(job)
            continue

        # Hybrid decision: SPT + Least loaded
        best_machine, best_start_time, best_processing_time = min(eligible_machines, key=lambda x: (x[2] + machine_load[x[0]]/ (sum(machine_load.values()) if sum(machine_load.values()) > 0 else 1)))

        end_time = best_start_time + best_processing_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        machine_available_time[best_machine] = end_time
        machine_load[best_machine] += best_processing_time
        job_operation_index[job] += 1

        if job_operation_index[job] < len(jobs[job]):
            job_queue.append(job)
            # Re-prioritize if needed (example: based on remaining operations)
            job_queue.sort(key=lambda j: len(jobs[j]) - job_operation_index[j]) #Sort for remaining operations.

    return schedule
