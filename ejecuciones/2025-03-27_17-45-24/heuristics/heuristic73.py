
def heuristic(input_data):
    """FJSSP heuristic: Combines EFT, load balancing, and shortest remaining time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    remaining_times = {}
    for job, ops in jobs_data.items():
        remaining_times[job] = sum(times[0] for _, times in ops)

    completed_operations = {job: 0 for job in range(1, n_jobs + 1)}

    while any(completed_operations[job] < len(jobs_data[job]) for job in range(1, n_jobs + 1)):
        eligible_operations = []
        for job in range(1, n_jobs + 1):
            if completed_operations[job] < len(jobs_data[job]):
                eligible_operations.append(job)

        if not eligible_operations:
            break
            
        job = min(eligible_operations, key=lambda j: remaining_times[j]) # Shortest remaining time

        op_idx = completed_operations[job]
        machines, times = jobs_data[job][op_idx]

        best_machine = None
        min_end_time = float('inf')
        best_start_time = 0
        best_processing_time = 0

        # EFT with load balancing
        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + processing_time

            # Load balancing consideration
            load_factor = machine_load[machine]
            
            #Combines EFT, and Load
            if end_time + 0.05*load_factor < min_end_time:
                min_end_time = end_time + 0.05*load_factor
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time
        
        if best_machine is None:
            best_machine=machines[0]
            best_processing_time = times[0]
            best_start_time=max(machine_available_time[machines[0]], job_completion_time[job])
        
        schedule[job] = schedule.get(job, [])
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job] = best_start_time + best_processing_time
        machine_load[best_machine] += best_processing_time
        remaining_times[job] -= best_processing_time
        completed_operations[job] += 1

    return schedule
