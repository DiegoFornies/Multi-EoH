
def heuristic(input_data):
    """
    A heuristic for FJSSP that considers machine workload
    and job progress to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    machine_load = {m: 0 for m in range(n_machines)} # track machine workload
    
    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, operation in enumerate(jobs_data[job]):
            machines, times = operation
            op_num = op_idx + 1
            
            best_machine = None
            min_end_time = float('inf')
            
            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time

                # Prioritize machines with less load and earlier completion
                load_factor = machine_load[machine]
                if end_time + load_factor < min_end_time:  # consider workload
                    min_end_time = end_time + load_factor
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            if best_machine is not None:
                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': best_start_time,
                    'End Time': best_start_time + best_processing_time,
                    'Processing Time': best_processing_time
                })
                
                machine_available_time[best_machine] = best_start_time + best_processing_time
                job_completion_time[job] = best_start_time + best_processing_time
                machine_load[best_machine] += best_processing_time
    return schedule
