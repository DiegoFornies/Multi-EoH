
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing idle time on machines
    and job completion times. It iteratively assigns operations to
    machines that become available the earliest, considering both machine
    availability and job precedence.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    operation_index = {j: 0 for j in range(1, n_jobs + 1)}
    
    unassigned_operations = []
    for job in range(1, n_jobs + 1):
        unassigned_operations.append((job, 0))

    while unassigned_operations:
        
        eligible_operations = []
        for job, op_index in unassigned_operations:
            
            if op_index < len(jobs_data[job]):
                eligible_operations.append((job, op_index))
                
        if not eligible_operations:
            break
        
        best_operation = None
        earliest_finish_time = float('inf')
        best_machine = None
        
        for job, op_index in eligible_operations:
            machines, times = jobs_data[job][op_index]

            for m_idx, m in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[m], job_completion_time[job])
                finish_time = start_time + processing_time

                if finish_time < earliest_finish_time:
                    earliest_finish_time = finish_time
                    best_operation = (job, op_index)
                    best_machine = m
                    best_processing_time = processing_time
                    best_start_time = start_time

        job, op_index = best_operation
        
        schedule[job].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': earliest_finish_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = earliest_finish_time
        job_completion_time[job] = earliest_finish_time

        unassigned_operations.remove((job, op_index))
        unassigned_operations.append((job, op_index + 1))
    
    return schedule
