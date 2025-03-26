
def heuristic(input_data):
    """Combines SPT, earliest start, and dynamic machine load consideration."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    job_total_processing_times = {}
    for job, operations in jobs.items():
        total_time = 0
        for machines, times in operations:
            total_time += min(times)
        job_total_processing_times[job] = total_time

    available_jobs = sorted(list(jobs.keys()), key=lambda x: job_total_processing_times[x])

    job_operations_scheduled = {job: 0 for job in jobs}
    
    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        for job_id in available_jobs:
            op_index = job_operations_scheduled[job_id]

            if op_index >= len(jobs[job_id]):
                continue

            if job_id not in schedule:
                schedule[job_id] = []

            operation_data = jobs[job_id][op_index]
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_weighted_time = float('inf')

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                processing_time = possible_times[i]

                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time
                
                # Dynamic weight based on machine load
                load_factor = machine_load[machine] / sum(machine_load.values()) if sum(machine_load.values()) > 0 else 0
                weighted_time = start_time + 0.7 * processing_time + 0.3 * load_factor*processing_time
                

                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            machine_available_times[best_machine] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_times[job_id] = best_start_time + best_processing_time
            job_operations_scheduled[job_id] += 1
            
            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

    return schedule
