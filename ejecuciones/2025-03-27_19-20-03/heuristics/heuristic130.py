
def heuristic(input_data):
    """Schedules jobs minimizing makespan and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}
    machine_load = {m: 0 for m in range(n_machines)}
    
    priority_list = [] # (priority, job)
    
    # Use Weighted Shortest Processing Time (WSPT) and consider machine load
    for job in jobs:
        ops = jobs[job]
        machines, times = ops[0]
        min_time = float('inf')
        for time in times:
            min_time = min(min_time,time)
        priority = min_time / (sum(times)/len(times))
        priority_list.append((priority, job))

    priority_list.sort()
    
    while priority_list:
        priority, job = priority_list.pop(0)
        
        if job not in schedule:
            schedule[job] = []
        
        op_idx = job_ops[job]
        machines, times = jobs[job][op_idx]

        best_machine = None
        min_start_time = float('inf')
        
        # Select machine considering machine load and start time.
        for m, t in zip(machines, times):
            start_time = max(machine_time[m], job_completion_time[job])
            # Weight start time by machine load to balance the workload
            weighted_start_time = start_time * (1 + 0.1 * machine_load[m] / (sum(machine_load.values())/len(machine_load) + 1e-6) if sum(machine_load.values()) > 0 else start_time)
            
            if weighted_start_time < min_start_time:
                min_start_time = weighted_start_time
                best_machine = m
                best_time = t
        
        if best_machine is None:
            raise ValueError("No feasible machine found.")
            
        start_time = max(machine_time[best_machine], job_completion_time[job])
        end_time = start_time + best_time
        
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })
        
        machine_time[best_machine] = end_time
        machine_load[best_machine] += best_time
        job_completion_time[job] = end_time
        job_ops[job] += 1
        
        if job_ops[job] < len(jobs[job]):
            next_machines, next_times = jobs[job][job_ops[job]]
            min_time = float('inf')
            for time in next_times:
                min_time = min(min_time,time)
            priority = (job_completion_time[job] + min_time) / (sum(next_times)/len(next_times))
            priority_list.append((priority, job))
            priority_list.sort()

    return schedule
