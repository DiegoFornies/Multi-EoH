
def heuristic(input_data):
    """Heuristic for FJSSP using a global makespan reduction approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Stores eligible ops by job
    remaining_operations = {}
    for job_id, operations in jobs_data.items():
        remaining_operations[job_id] = list(range(len(operations)))

    while any(remaining_operations.values()):
        # Find the operation that leads to minimal makespan increase
        best_job = None
        best_op_idx = None
        best_machine = None
        min_makespan_increase = float('inf')
        best_processing_time = None

        for job_id, ops_indices in remaining_operations.items():
            if not ops_indices:
                continue
            op_idx = ops_indices[0]
            machines, times = jobs_data[job_id][op_idx]
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                temp_machine_available = machine_available_time[machine]
                machine_available_time[machine] = end_time
                temp_job_completion = job_completion_time[job_id]
                job_completion_time[job_id] = end_time
                
                makespan_increase = end_time - max(temp_machine_available, temp_job_completion)
                
                if makespan_increase < min_makespan_increase:
                    min_makespan_increase = makespan_increase
                    best_job = job_id
                    best_op_idx = op_idx
                    best_machine = machine
                    best_processing_time = processing_time

                machine_available_time[machine] = temp_machine_available
                job_completion_time[job_id] = temp_job_completion
        
        # Schedule the operation
        start_time = max(machine_available_time[best_machine], job_completion_time[best_job])
        end_time = start_time + best_processing_time
        machine_available_time[best_machine] = end_time
        job_completion_time[best_job] = end_time

        if best_job not in schedule:
            schedule[best_job] = []
        schedule[best_job].append({
            'Operation': best_op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        remaining_operations[best_job].pop(0)
    return schedule
