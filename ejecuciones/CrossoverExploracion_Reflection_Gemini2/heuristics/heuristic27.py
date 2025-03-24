
def heuristic(input_data):
    """
    A scheduling heuristic that prioritizes jobs with shorter total processing times
    and assigns operations to machines based on earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    # Calculate total processing time for each job
    job_processing_times = {}
    for job, operations in jobs_data.items():
        total_time = 0
        for machines, times in operations:
            total_time += min(times)  # Take the minimum processing time if multiple machines
        job_processing_times[job] = total_time
    
    # Sort jobs based on total processing time (shortest first)
    sorted_jobs = sorted(job_processing_times.items(), key=lambda item: item[1])
    
    schedule = {}
    machine_available_times = {m: 0 for m in range(1, n_machines + 1)} # Machine starts from 1 according to the input example

    for job, _ in sorted_jobs:
        schedule[job] = []
        job_completion_time = 0

        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1
            
            # Find the machine with the earliest available time among feasible machines
            best_machine = None
            earliest_time = float('inf')
            best_processing_time = None

            for i, machine in enumerate(machines):
                available_time = machine_available_times[machine]
                start_time = max(available_time, job_completion_time)
                
                if start_time < earliest_time:
                    earliest_time = start_time
                    best_machine = machine
                    best_processing_time = times[i]
            
            start_time = earliest_time
            end_time = start_time + best_processing_time
            
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })
            
            machine_available_times[best_machine] = end_time
            job_completion_time = end_time
    
    return schedule
