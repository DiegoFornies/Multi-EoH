
def heuristic(input_data):
    """A heuristic that schedules operations based on earliest possible start time, 
       considering both machine and job availability and shortest processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs_data:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs_data[job]):
            machines, times = operation

            # Find the earliest possible start time for the operation
            best_start_time = float('inf')
            best_machine = None
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule the operation on the best machine
            start_time = best_start_time
            end_time = start_time + best_processing_time
            machine = best_machine
            processing_time = best_processing_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine and job completion times
            machine_available_time[machine] = end_time
            job_completion_time[job] = end_time

    return schedule
