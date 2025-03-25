
def heuristic(input_data):
    """Schedules jobs based on shortest operation remaining."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    remaining_operations = {job: list(range(1, len(jobs[job]) + 1)) for job in jobs}
    
    while any(remaining_operations.values()):
        eligible_operations = []
        for job in jobs:
            if remaining_operations[job]:
                op_num = remaining_operations[job][0]
                op_idx = op_num - 1
                eligible_operations.append((job, op_num))
        
        # Prioritize based on shortest processing time across available machines
        best_job = None
        best_op = None
        min_duration = float('inf')
        assigned_machine = None
        process_time = None
        
        for job, op_num in eligible_operations:
            op_idx = op_num - 1
            machines, times = jobs[job][op_idx]
            
            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])
                duration = times[m_idx]
                if duration < min_duration:
                    min_duration = duration
                    best_job = job
                    best_op = op_num
                    assigned_machine = machine
                    process_time = times[m_idx]
        
        if best_job is not None:
            op_idx = best_op - 1
            start_time = max(machine_available_time[assigned_machine], job_completion_time[best_job])
            end_time = start_time + process_time
            
            if best_job not in schedule:
                schedule[best_job] = []
                
            schedule[best_job].append({
                'Operation': best_op,
                'Assigned Machine': assigned_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': process_time
            })
            
            machine_available_time[assigned_machine] = end_time
            job_completion_time[best_job] = end_time
            remaining_operations[best_job].pop(0) # Remove operation
            
    return schedule
