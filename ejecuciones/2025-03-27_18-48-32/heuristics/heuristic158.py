
def heuristic(input_data):
    """Heuristic minimizing makespan and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs.keys()}
    schedule = {job: [] for job in jobs.keys()}
    
    operations = []
    for job_id in jobs:
        for op_idx, operation in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, operation))

    operations.sort(key=lambda x: min(x[2][1]))

    for job_id, op_idx, operation in operations:
        possible_machines = operation[0]
        possible_times = operation[1]

        best_machine = None
        min_end_time = float('inf')
        best_start_time = float('inf')
        
        for i, machine_id in enumerate(possible_machines):
            processing_time = possible_times[i]
            start_time = max(machine_available_times[machine_id], job_completion_times[job_id])
            end_time = start_time + processing_time
            
            if end_time < min_end_time or (end_time == min_end_time and start_time < best_start_time):
                min_end_time = end_time
                best_start_time = start_time
                best_machine = machine_id

        processing_time = possible_times[possible_machines.index(best_machine)]
        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + processing_time
        
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
