
def heuristic(input_data):
    """Heuristic for FJSSP minimizing makespan, idle time, and balancing load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        operations = jobs[job_id]
        
        for op_index, operation in enumerate(operations):
            eligible_machines = operation[0]
            processing_times = operation[1]
            
            best_machine = None
            min_completion_time = float('inf')

            for machine_index, machine_id in enumerate(eligible_machines):
                completion_time = max(machine_available_time[machine_id], job_completion_time[job_id]) + processing_times[machine_index]
                
                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine_id
                    best_processing_time = processing_times[machine_index]
            
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time
            
            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })
            
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
