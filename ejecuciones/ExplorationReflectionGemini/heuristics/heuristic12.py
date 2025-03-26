
def heuristic(input_data):
    """
    A heuristic for FJSSP that considers machine load and job precedence.

    It assigns operations to the least loaded machine among available options,
    prioritizing jobs with earlier due dates or smaller total processing time.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    
    # Calculate total processing time for each job for prioritization
    job_total_processing_times = {}
    for job, operations in jobs.items():
        total_time = 0
        for machines, times in operations:
            total_time += min(times)  # Take the minimum time as an estimate
        job_total_processing_times[job] = total_time

    # Jobs are prioritized based on shortest processing time
    available_jobs = sorted(list(jobs.keys()), key=lambda x: job_total_processing_times[x])  # Sort by processing time

    # Schedule operations
    while available_jobs:
        job = available_jobs.pop(0)
        job_schedule = schedule[job]
        next_op_index = len(job_schedule)
        
        if next_op_index >= len(jobs[job]):
            continue
            
        machines, times = jobs[job][next_op_index]
        op_num = next_op_index + 1
        
        # Find the machine with the least load
        best_machine = None
        best_time = float('inf')
        
        for i, m in enumerate(machines):
            available_time = machine_load[m]
            start_time = max(job_completion_times[job], available_time)
            if start_time < best_time:
                best_time = start_time
                best_machine = m
                processing_time = times[i] #Get the correct processing time

        
        start_time = max(job_completion_times[job], machine_load[best_machine])
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        machine_load[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
