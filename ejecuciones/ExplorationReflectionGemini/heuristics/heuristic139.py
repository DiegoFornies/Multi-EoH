
def heuristic(input_data):
    """FJSSP heuristic: SPT with dynamic machine load balancing."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)} # Track machine load
    schedule = {j: [] for j in jobs}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        best_op = None
        best_start_time = float('inf')
        best_processing_time = float('inf')
        best_machine = None
        best_time = None

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Prioritize based on SPT and machine load.
            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                processing_time = time
                #Dynamic load balancing weight
                load_factor = machine_load[machine]/sum(machine_load.values()) if sum(machine_load.values()) >0 else 0 #machine_load[machine] / (sum(machine_load.values()) + 1e-9)
                # Combine SPT and load balancing. Prioritize shorter jobs and less loaded machines.
                priority = processing_time + load_factor*100 #weight the load factor, 0.1, 1 ,10 ,100

                if start_time + priority < best_start_time + best_processing_time  or best_op is None: #original: start_time < best_start_time or (start_time == best_start_time and processing_time < best_processing_time): #start_time + priority < best_start_time + best_processing_time
                    best_start_time = start_time
                    best_processing_time = processing_time
                    best_op = op_data
                    best_machine = machine
                    best_time = time

        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_load[best_machine] += best_time # Update machine load

        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
