
def heuristic(input_data):
    """FJSSP heuristic minimizing makespan using a greedy approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Sort operations by shortest processing time on the best machine
    eligible_operations = []
    for job in jobs:
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            best_machine = None
            min_processing_time = float('inf')
            
            for i, machine in enumerate(machines):
                if times[i] < min_processing_time:
                    min_processing_time = times[i]
                    best_machine = machine
            
            eligible_operations.append((job, op_idx, best_machine, min_processing_time))

    eligible_operations.sort(key=lambda x: x[3])  # Sort by min processing time

    for job, op_idx, best_machine, processing_time in eligible_operations:
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + processing_time
        
        if job not in schedule:
            schedule[job] = []
            
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
