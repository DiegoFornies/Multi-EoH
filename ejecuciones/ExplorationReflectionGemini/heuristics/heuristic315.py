
def heuristic(input_data):
    """A rolling-horizon heuristic for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    
    uncompleted_operations = []
    for job_id, operations in jobs.items():
        for op_idx in range(len(operations)):
            uncompleted_operations.append((job_id, op_idx))
    
    while uncompleted_operations:
        # Sort operations by earliest possible start time (SPT)
        uncompleted_operations.sort(key=lambda item: calculate_est(item, jobs, machine_available_times, job_completion_times))
        
        job_id, op_idx = uncompleted_operations.pop(0) # Select the operation with earliest start time.
        machines, times = jobs[job_id][op_idx]
        
        # Select machine with smallest load (Load balancing).
        best_machine, best_time = find_best_machine(machines, times, machine_available_times, job_completion_times[job_id])
        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_time
        
        # Update times and create the schedule.
        op_num = op_idx + 1
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })
        
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        
        # Update the uncompleted operation list.
        new_uncompleted_operations = []
        for job_id, op_idx_check in uncompleted_operations:
            if op_idx_check < len(jobs[job_id]):
                new_uncompleted_operations.append((job_id, op_idx_check))
        uncompleted_operations = new_uncompleted_operations
        
    return schedule
    
def calculate_est(operation, jobs, machine_available_times, job_completion_times):
    job_id, op_idx = operation
    machines, times = jobs[job_id][op_idx]
    earliest_start_time = float('inf')
    
    for machine_idx, (machine, time) in enumerate(zip(machines, times)):
        start_time = max(machine_available_times[machine], job_completion_times[job_id])
        earliest_start_time = min(earliest_start_time, start_time)
        
    return earliest_start_time

def find_best_machine(machines, times, machine_available_times, job_completion_time):
    best_machine = None
    best_time = float('inf')
    min_load = float('inf')
    processing_time = None
    
    for machine_idx, (machine, time) in enumerate(zip(machines, times)):
        start_time = max(machine_available_times[machine], job_completion_time)
        
        if machine_available_times[machine] < min_load:
            min_load = machine_available_times[machine]
            best_machine = machine
            best_time = time
            
    return best_machine, best_time
