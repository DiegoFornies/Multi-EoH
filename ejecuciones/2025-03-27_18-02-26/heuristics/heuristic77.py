
def heuristic(input_data):
    """Schedules operations based on shortest processing time first."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    available_operations = []
    for job in jobs:
        available_operations.append((job, 0))

    scheduled_operations = set()
    while available_operations:
        # Find the available operation with shortest processing time.
        best_op = None
        min_duration = float('inf')

        for job, op_idx in list(available_operations):
            machines, times = jobs[job][op_idx]
            
            for m_idx, m in enumerate(machines):
                start_time = max(machine_time[m], job_completion_time[job])
                duration = times[m_idx]
                
                if duration < min_duration:
                    min_duration = duration
                    best_op = (job, op_idx, m, duration, start_time)

        if best_op is None:
           break

        job, op_idx, assigned_machine, processing_time, start_time = best_op
        end_time = start_time + processing_time

        if job not in schedule:
            schedule[job] = []
        
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        machine_time[assigned_machine] = end_time
        job_completion_time[job] = end_time
        available_operations.remove((job, op_idx))

        if op_idx + 1 < len(jobs[job]):
            available_operations.append((job, op_idx + 1))

    return schedule
