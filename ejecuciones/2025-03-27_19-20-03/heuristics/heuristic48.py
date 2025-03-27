
def heuristic(input_data):
    """Assigns operations greedily, minimizing makespan using CRPT."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    remaining_processing_times = {}
    for job in range(1, n_jobs + 1):
        remaining_processing_times[job] = sum(min(times) for machines, times in jobs_data[job])
    
    job_queue = list(range(1, n_jobs + 1))

    while job_queue:
        # Choose job with the Critical Remaining Processing Time (CRPT)
        current_job = min(job_queue, key=lambda job: remaining_processing_times[job])

        job_queue.remove(current_job)
        
        for op_index, operation in enumerate(jobs_data[current_job]):
            machines, times = operation
            
            best_machine = None
            min_finish_time = float('inf')
            best_start_time = None
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[current_job])
                finish_time = start_time + processing_time

                if finish_time < min_finish_time:
                    min_finish_time = finish_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            schedule[current_job].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_finish_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = min_finish_time
            job_completion_time[current_job] = min_finish_time
            remaining_processing_times[current_job] -= min(times) #Update the value of remain processing time

    return schedule
