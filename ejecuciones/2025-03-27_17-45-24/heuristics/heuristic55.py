
def heuristic(input_data):
    """Schedules jobs minimizing makespan with a job-based approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    
    for job in range(1, n_jobs + 1):
        schedule[job] = []
        current_time = 0
        for op_idx, operation in enumerate(jobs_data[job]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_start_time = float('inf')
            
            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], current_time)

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': min_start_time,
                'End Time': min_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })
            
            machine_available_time[best_machine] = min_start_time + best_processing_time
            current_time = min_start_time + best_processing_time
            job_completion_time[job] = current_time
    return schedule
