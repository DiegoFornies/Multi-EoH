
def heuristic(input_data):
    """
    A scheduling heuristic that prioritizes machines with the earliest available time 
    and jobs with the fewest remaining operations. 
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_next_operation = {job: 0 for job in jobs_data}
    job_completion_times = {job: 0 for job in jobs_data}
    schedule = {job: [] for job in jobs_data}

    uncompleted_jobs = set(jobs_data.keys())
    
    while uncompleted_jobs:
        eligible_operations = []
        for job in uncompleted_jobs:
            op_idx = job_next_operation[job]
            eligible_operations.append((job, op_idx))
        
        # Prioritize jobs with fewer remaining operations
        eligible_operations.sort(key=lambda x: len(jobs_data[x[0]]) - x[1])

        job, op_idx = eligible_operations[0]
        machines, times = jobs_data[job][op_idx]
        
        # Find the machine with earliest available time among possible machines
        best_machine = None
        earliest_start = float('inf')
        processing_time = 0

        for m_idx, machine in enumerate(machines):
          start_time = max(machine_available_times[machine], job_completion_times[job])
          if start_time < earliest_start:
            earliest_start = start_time
            best_machine = machine
            processing_time = times[m_idx]
        
        start = earliest_start
        end = start + processing_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start,
            'End Time': end,
            'Processing Time': processing_time
        })
        
        machine_available_times[best_machine] = end
        job_completion_times[job] = end
        job_next_operation[job] += 1

        if job_next_operation[job] == len(jobs_data[job]):
            uncompleted_jobs.remove(job)

    return schedule
