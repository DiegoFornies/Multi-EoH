
def heuristic(input_data):
    """A heuristic to solve FJSSP, minimizing makespan."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {}

    for job_id in jobs:
        schedule[job_id] = []

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((job_id, op_idx, op_data))

    # Prioritize operations with fewer machine choices
    operations.sort(key=lambda x: len(x[2][0]))  # Sort by num of possible machines

    while operations:
        best_op = None
        earliest_end_time = float('inf')
        best_machine = None
        
        for job_id, op_idx, op_data in operations:
            machines, times = op_data
            
            # Find the best machine for this operation: earliest completion time
            best_local_machine = None
            earliest_local_end_time = float('inf')
            
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                available_time = machine_available_times[machine]
                
                # Consider Job completion time (sequencing constraint)
                start_time = max(available_time, job_completion_times[job_id])
                end_time = start_time + processing_time
                
                if end_time < earliest_local_end_time:
                    earliest_local_end_time = end_time
                    best_local_machine = machine
            
            # Keep track of the overall best
            if earliest_local_end_time < earliest_end_time:
                earliest_end_time = earliest_local_end_time
                best_op = (job_id, op_idx, op_data)
                best_machine = best_local_machine

        # Schedule the best operation
        job_id, op_idx, op_data = best_op
        machines, times = op_data
        
        m_idx = machines.index(best_machine)
        processing_time = times[m_idx]
        
        available_time = machine_available_times[best_machine]
        start_time = max(available_time, job_completion_times[job_id])
        end_time = start_time + processing_time
        
        operation_number = op_idx + 1
        schedule[job_id].append({
            'Operation': operation_number,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

        operations.remove(best_op)

    return schedule
