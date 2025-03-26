
def heuristic(input_data):
    """Minimize makespan using a greedy, machine-centric approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_schedules = {m: [] for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    job_operation_index = {j: 0 for j in range(1, n_jobs + 1)} #Track what operation of each job is next
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    completed_jobs = set()

    while len(completed_jobs) < n_jobs:
        # For each machine, check if an operation is ready to be scheduled
        for machine_id in range(n_machines):
            eligible_jobs = []
            for job_id in range(1, n_jobs + 1):
                if job_id in completed_jobs:
                    continue

                operation_index = job_operation_index[job_id]
                job_ops = jobs[job_id]
                if operation_index >= len(job_ops):
                    completed_jobs.add(job_id) #Job is done.
                    continue
                
                machines, times = job_ops[operation_index]
                if machine_id in machines:
                    eligible_jobs.append(job_id)

            if eligible_jobs:
                # Find the job with the shortest processing time on this machine.
                best_job = None
                min_time = float('inf')

                for job_id in eligible_jobs:
                    operation_index = job_operation_index[job_id]
                    machines, times = jobs[job_id][operation_index]
                    time_index = machines.index(machine_id)
                    processing_time = times[time_index]

                    if processing_time < min_time:
                        min_time = processing_time
                        best_job = job_id

                # Schedule the operation
                operation_index = job_operation_index[best_job]
                machines, times = jobs[best_job][operation_index]
                time_index = machines.index(machine_id)
                processing_time = times[time_index]
                
                start_time = 0
                if machine_schedules[machine_id]:
                   start_time = machine_schedules[machine_id][-1]['End Time']
                start_time = max(start_time, job_completion_times[best_job])


                end_time = start_time + processing_time
                machine_schedules[machine_id].append({
                    'Operation': operation_index + 1,
                    'Job': best_job,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })

                schedule[best_job].append({
                    'Operation': operation_index + 1,
                    'Assigned Machine': machine_id,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })

                job_completion_times[best_job] = end_time
                job_operation_index[best_job] += 1


    return schedule
