
def heuristic(input_data):
    """Heuristic for FJSSP: Prioritizes jobs with fewer operations."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    job_priority = sorted(jobs.keys(), key=lambda job_id: len(jobs[job_id]))
    
    for job_id in job_priority:
        schedule[job_id] = []
        for op_index, operation in enumerate(jobs[job_id]):
            eligible_machines = operation[0]
            processing_times = operation[1]
            
            best_machine = None
            min_end_time = float('inf')

            for machine_index, machine_id in enumerate(eligible_machines):
                start_time = max(machine_time[machine_id], job_completion_time[job_id])
                end_time = start_time + processing_times[machine_index]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine_id
                    best_processing_time = processing_times[machine_index]
                    best_start_time = start_time
            
            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_end_time,
                'Processing Time': best_processing_time
            })
            
            machine_time[best_machine] = min_end_time
            job_completion_time[job_id] = min_end_time

    return schedule
