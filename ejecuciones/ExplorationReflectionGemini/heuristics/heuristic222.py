
def heuristic(input_data):
    """Adaptive heuristic: SPT + Load Balancing with dynamic weight."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    schedule = {job: [] for job in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_cost = float('inf')
            
            #Dynamic adjust weight for SPT and load balancing
            load_weight = 0.1 + (op_idx/len(jobs[job]))*0.1

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time
                cost = start_time + load_weight * machine_load[machine] + processing_time
                
                if cost < min_cost:
                    min_cost = cost
                    best_machine = machine
                    best_start_time = start_time
                    best_end_time = end_time
                    best_processing_time = processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_end_time
            machine_load[best_machine] = best_end_time
            job_completion_time[job] = best_end_time
    return schedule
