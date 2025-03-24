
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem.
    Prioritizes jobs with fewer remaining operations and assigns operations to machines based on earliest available time and shortest processing time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    remaining_operations = {j: len(ops) for j, ops in jobs_data.items()}
    
    schedule = {}
    
    scheduled_operations = 0
    total_operations = sum(remaining_operations.values())

    while scheduled_operations < total_operations:
        eligible_jobs = [j for j in jobs_data if remaining_operations[j] > 0]
        
        if not eligible_jobs:
            break
        
        # Prioritize jobs with fewer remaining operations
        job = min(eligible_jobs, key=lambda j: remaining_operations[j])
        
        op_idx = len(jobs_data[job]) - remaining_operations[job]
        machines, times = jobs_data[job][op_idx]
        
        # Find the machine with the earliest available time and shortest processing time
        best_machine, best_time, earliest_start = None, float('inf'), float('inf')
        
        for i, m in enumerate(machines):
            start_time = max(machine_available_time[m], job_last_end_time[job])
            if start_time < earliest_start or (start_time == earliest_start and times[i] < best_time):
                earliest_start = start_time
                best_machine = m
                best_time = times[i]
                best_machine_index = i
        
        start_time = max(machine_available_time[best_machine], job_last_end_time[job])
        end_time = start_time + best_time
        
        if job not in schedule:
            schedule[job] = []
            
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })
        
        machine_available_time[best_machine] = end_time
        job_last_end_time[job] = end_time
        remaining_operations[job] -= 1
        scheduled_operations += 1

    return schedule
