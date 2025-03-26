
def heuristic(input_data):
    """Combines earliest availability and load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}  # Keep track of machine load
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_completion_time = float('inf')
            
            # Find machine minimizing completion time + load balance term
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                completion_time = start_time + processing_time
                
                # Load balance term: Prefer machines with lower load
                load_balance_factor = machine_load[machine]  # Simpler load measure
                
                # Combine completion time and load balance factor
                combined_metric = completion_time + 0.1 * load_balance_factor  # Adjust weight 

                if combined_metric < min_completion_time:
                    min_completion_time = combined_metric
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

            # Assign to best machine
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability, load and job completion time
            machine_available_time[best_machine] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_time[job] = best_start_time + best_processing_time

    return schedule
