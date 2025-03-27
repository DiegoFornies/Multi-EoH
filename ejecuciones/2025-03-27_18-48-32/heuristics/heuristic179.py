
def heuristic(input_data):
    """Heuristic: SPT with job urgency and dynamic machine selection."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_remaining_operations = {j: len(jobs[j]) for j in jobs}
    job_start_time = {j:0 for j in jobs}
    
    unassigned_operations = []
    for job_id in jobs:
        for op_idx in range(len(jobs[job_id])):
            unassigned_operations.append((job_id, op_idx))

    while unassigned_operations:
        # Prioritize jobs with fewer remaining operations
        job_id, op_idx = min(unassigned_operations, key=lambda x: job_remaining_operations[x[0]])
        operation = jobs[job_id][op_idx]
        possible_machines = operation[0]
        possible_times = operation[1]
        
        # Dynamic Machine Selection: SPT based on earliest possible finish time.
        best_machine = None
        min_finish_time = float('inf')
        
        for machine in possible_machines:
            processing_time = possible_times[possible_machines.index(machine)]
            start_time = max(machine_available_time[machine], job_start_time[job_id])
            finish_time = start_time + processing_time
            if finish_time < min_finish_time:
                min_finish_time = finish_time
                best_machine = machine
                
        processing_time = possible_times[possible_machines.index(best_machine)]
        start_time = max(machine_available_time[best_machine], job_start_time[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        
        job_remaining_operations[job_id] -= 1
        job_start_time[job_id] = end_time

        unassigned_operations.remove((job_id, op_idx))

    return schedule
