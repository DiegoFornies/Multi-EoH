
def heuristic(input_data):
    """Combines SPT sorting with machine load balancing for FJSSP."""
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)}
    schedule = {}
    operation_index = {j: 0 for j in jobs}

    for job_id in jobs:
        schedule[job_id] = []

    operations = []
    for job_id, job_ops in jobs.items():
        if operation_index[job_id] < len(job_ops):
            op_idx = operation_index[job_id]
            op_data = job_ops[op_idx]
            operations.append((job_id, op_idx, op_data))

    operations = sorted(operations, key=lambda x: min(x[2][1]))
    
    while operations:
        best_job, best_op_idx, best_op_data = None, None, None
        best_machine, best_start_time, best_end_time, best_processing_time = None, None, None, None
        min_impact = float('inf')
    
        for job_id, op_idx, op_data in operations:
            available_machines, processing_times = op_data
    
            for machine_idx, machine in enumerate(available_machines):
                processing_time = processing_times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                machine_load_impact = machine_load[machine] + processing_time
                impact = machine_load_impact

                if impact < min_impact:
                    min_impact = impact
                    best_job, best_op_idx, best_op_data = job_id, op_idx, op_data
                    best_machine = machine
                    best_start_time = start_time
                    best_end_time = end_time
                    best_processing_time = processing_time
    
        schedule[best_job].append({
            'Operation': best_op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_end_time,
            'Processing Time': best_processing_time
        })
    
        machine_available_time[best_machine] = best_end_time
        job_completion_time[best_job] = best_end_time
        machine_load[best_machine] += best_processing_time
    
        operations.remove((best_job, best_op_idx, best_op_data))

        operation_index[best_job] += 1
        if operation_index[best_job] < len(jobs[best_job]):
            next_op_idx = operation_index[best_job]
            next_op_data = jobs[best_job][next_op_idx]
            operations.append((best_job, next_op_idx, next_op_data))
        operations = sorted(operations, key = lambda x: min(x[2][1]))

    return schedule
