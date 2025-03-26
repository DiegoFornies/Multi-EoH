
def heuristic(input_data):
    """
    Schedules jobs by prioritizing operations with the fewest machine options
    and assigning them to the machine that minimizes idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    
    unscheduled_operations = []
    for job_id, operations in jobs_data.items():
        for op_idx, op_data in enumerate(operations):
            unscheduled_operations.append({
                'job_id': job_id,
                'op_idx': op_idx,
                'machines': op_data[0],
                'times': op_data[1]
            })
    
    # Prioritize operations with fewer machine choices first
    unscheduled_operations.sort(key=lambda x: len(x['machines']))

    while unscheduled_operations:
        best_op = None
        best_machine = None
        earliest_start = float('inf')
        
        for op in unscheduled_operations:
            job_id = op['job_id']
            op_idx = op['op_idx']
            machines = op['machines']
            times = op['times']
            
            # Find the machine that minimizes idle time for this operation
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_op = op
                    best_machine = machine
                    best_processing_time = processing_time
                    
        # Schedule the operation on the chosen machine
        job_id = best_op['job_id']
        op_idx = best_op['op_idx']
        operation_number = op_idx + 1
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': operation_number,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        unscheduled_operations.remove(best_op)
    
    return schedule
