
def heuristic(input_data):
    """Schedules jobs by considering machine idle time and job urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}
    machine_idle_times = {m: [] for m in range(n_machines)}

    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 1))

    while eligible_operations:
        best_op = None
        best_start = float('inf')
        best_machine = None
        best_time = None
        best_job = None

        for job, op_num in eligible_operations:
            machines, times = jobs_data[job][op_num - 1]
            
            best_local_machine = None
            best_local_start = float('inf')
            best_local_time = None

            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_times[job])

                # Prioritize machines with more idle time and urgent jobs
                idle_time_score = sum([end - start for start, end in machine_idle_times[m] if end > start_time]) #total amount of idle time from start_time forward.
                job_urgency = job_completion_times[job]
                
                # Calculate a combined score
                score = start_time - (idle_time_score * 0.1) - (job_urgency * 0.05) # Favor earlier start, idle machine, urgent job

                if score < best_local_start:
                    best_local_start = score
                    best_local_machine = m
                    best_local_time = times[m_idx]

            if best_local_start < best_start:
                best_start = best_local_start
                best_op = op_num
                best_machine = best_local_machine
                best_time = best_local_time
                best_job = job

        start_time = max(machine_available_times[best_machine], job_completion_times[best_job])
        end_time = start_time + best_time
        scheduled_operations[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine available time and idle times
        machine_available_times[best_machine] = end_time
        job_completion_times[best_job] = end_time
        
        #Record idle time if any.
        if start_time > 0 and machine_available_times[best_machine] - best_time != start_time :
           machine_idle_times[best_machine].append((machine_available_times[best_machine] - best_time, start_time))
        else :
            machine_idle_times[best_machine].append((0,0))

        eligible_operations.remove((best_job, best_op))

        if best_op < len(jobs_data[best_job]):
            eligible_operations.append((best_job, best_op + 1))

    return scheduled_operations
