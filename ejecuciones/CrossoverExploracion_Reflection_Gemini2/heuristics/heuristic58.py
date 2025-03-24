
def heuristic(input_data):
    """Schedules jobs with priority to shortest operation time on least loaded machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    schedule = {j: [] for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs_data[job_id]):
            op_num = op_idx + 1
            machines, processing_times = operation

            best_machine = None
            min_cost = float('inf') #cost based on machine load and processing time

            for i, machine in enumerate(machines):
                processing_time = processing_times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                cost = processing_time + machine_load[machine] 

                if cost < min_cost:
                    min_cost = cost
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })
            
            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job_id] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time

    return schedule
