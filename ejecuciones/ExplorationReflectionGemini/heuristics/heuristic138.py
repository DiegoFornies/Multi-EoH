
def heuristic(input_data):
    """Schedules jobs using a machine-based earliest available time heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    
    remaining_operations = {job_id: 0 for job_id in jobs}

    while True:
        eligible_operations = []
        for job_id in jobs:
            op_idx = remaining_operations[job_id]
            if op_idx < len(jobs[job_id]):
                eligible_operations.append((job_id, op_idx))

        if not eligible_operations:
            break

        best_operation = None
        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None
        
        for job_id, op_idx in eligible_operations:
            machines, times = jobs[job_id][op_idx]
            
            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_operation = (job_id, op_idx)
                    best_machine = machine
                    best_processing_time = time
                    
        job_id, op_idx = best_operation
        op_num = op_idx + 1

        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time
        
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        remaining_operations[job_id] += 1

    return schedule
