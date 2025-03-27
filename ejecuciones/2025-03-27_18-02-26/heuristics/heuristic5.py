
def heuristic(input_data):
    """Schedules jobs using a shortest processing time and earliest machine availability heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)} # Track cumulative load
    schedule = {}

    for job in jobs:
        schedule[job] = []

    job_completion_times = {job: 0 for job in jobs}

    operations = []
    for job, ops in jobs.items():
        for i, op in enumerate(ops):
            operations.append((job, i, op))

    #Sort by shortest processing time, job and operation order as tie breaker
    operations.sort(key=lambda x: min(x[2][1]))  

    for job, op_idx, op in operations:
        machines, times = op
        
        #Find the machine that minimizes the completion time of the current operation.
        best_machine, min_completion_time = None, float('inf')

        for m_idx, m in enumerate(machines):
          completion_time = max(machine_time[m], job_completion_times[job]) + times[m_idx]
          if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = m
                best_time = times[m_idx]

        start_time = max(machine_time[best_machine], job_completion_times[job])
        end_time = start_time + best_time
            
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time,
        })
            
        machine_time[best_machine] = end_time
        job_completion_times[job] = end_time
        machine_load[best_machine] += best_time
    
    return schedule
