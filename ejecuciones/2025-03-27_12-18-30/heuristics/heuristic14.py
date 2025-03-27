
def heuristic(input_data):
    """A heuristic to schedule jobs while minimizing makespan, idle time, and balancing machine load."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize schedule, machine availability, and job completion times
    schedule = {}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Create a list of operations to schedule, prioritizing earlier operations in each job
    operations = []
    for job_id, job_ops in jobs_data.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((job_id, op_idx, op_data))

    # Sort operations based on shortest processing time on the fastest available machine
    def sorting_key(op):
        job_id, op_idx, op_data = op
        machines, times = op_data
        
        best_machine, best_time = None, float('inf')
        for m, t in zip(machines, times):
            if machine_availability[m] <= job_completion_times[job_id] and t < best_time:
                best_machine, best_time = m, t
            elif machine_availability[m] > job_completion_times[job_id] and machine_availability[m] + t < best_time:
                best_machine, best_time = m, t
        
        if best_machine is None:
            for m, t in zip(machines, times):
                if machine_availability[m] + t < best_time:
                   best_machine, best_time = m, t
        
        return best_time if best_machine is not None else float('inf')

    operations.sort(key=sorting_key)

    # Schedule each operation based on earliest start time
    for job_id, op_idx, op_data in operations:
        machines, times = op_data
        op_num = op_idx + 1
        
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        
        for m, t in zip(machines, times):
            start_time = max(machine_availability[m], job_completion_times[job_id])
            
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = m
                best_processing_time = t
            
        # Update schedule, machine availability, and job completion time
        end_time = best_start_time + best_processing_time
        
        if job_id not in schedule:
            schedule[job_id] = []
            
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        machine_availability[best_machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
