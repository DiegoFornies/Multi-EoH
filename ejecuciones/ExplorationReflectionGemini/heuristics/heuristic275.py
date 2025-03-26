
def heuristic(input_data):
    """Schedules jobs minimizing makespan via dynamic priority."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_last_end = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    uncompleted_operations = {}
    for job_id in range(1, n_jobs + 1):
        uncompleted_operations[job_id] = [(op_idx + 1) for op_idx in range(len(jobs[job_id]))]

    all_operations = []
    for job_id in range(1, n_jobs + 1):
      for op_idx, operation_data in enumerate(jobs[job_id]):
        all_operations.append((job_id, op_idx + 1))

    while all_operations:
        eligible_operations = []

        for job_id in range(1, n_jobs + 1):
            if not uncompleted_operations[job_id]:
                continue
            
            next_operation_index = uncompleted_operations[job_id][0] -1
            
            operation_data = jobs[job_id][next_operation_index]
            
            machines = operation_data[0]
            eligible = True
            
            eligible_operations.append((job_id,next_operation_index + 1))
            
        #Prioritize operations with shortest processing time (SPT) on least loaded machine.
        best_operation = None
        min_weighted_time = float('inf')
        
        for job_id, op_idx in eligible_operations:
            operation_data = jobs[job_id][op_idx - 1]
            machines = operation_data[0]
            processing_times = operation_data[1]

            for i, machine in enumerate(machines):
                processing_time = processing_times[i]
                available_time = max(machine_available[machine], job_last_end[job_id])
                weighted_time = available_time + processing_time
                
                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_operation = (job_id, op_idx, machine, processing_time)

        job_id, op_idx, assigned_machine, processing_time = best_operation
        start_time = max(machine_available[assigned_machine], job_last_end[job_id])
        end_time = start_time + processing_time

        machine_available[assigned_machine] = end_time
        job_last_end[job_id] = end_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        uncompleted_operations[job_id].pop(0)

        found = False
        for job_op in all_operations:
            if job_op[0] == job_id and job_op[1] == op_idx:
                all_operations.remove(job_op)
                found = True
                break

    return schedule
