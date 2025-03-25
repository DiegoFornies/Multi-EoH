
def heuristic(input_data):
    """Combines shortest job and earliest start for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    job_processing_times = {}
    for job, ops in jobs_data.items():
        total_time = sum(min(times) for machines, times in ops)
        job_processing_times[job] = total_time

    sorted_jobs = sorted(job_processing_times.items(), key=lambda item: item[1])
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data.keys()}

    for job, _ in sorted_jobs:
        schedule[job] = []
        
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1

            best_machine = None
            earliest_start = float('inf')
            chosen_processing_time = None

            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_machine = machine
                    chosen_processing_time = times[i]
            
            start_time = earliest_start
            end_time = start_time + chosen_processing_time
            
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': chosen_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time
            
    return schedule
