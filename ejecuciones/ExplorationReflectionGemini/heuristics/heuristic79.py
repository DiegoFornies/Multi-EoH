
def heuristic(input_data):
    """Schedules jobs considering machine load balancing and makespan."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)}
    schedule = {j: [] for j in jobs}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        best_op = None
        best_start_time = float('inf')
        best_processing_time = float('inf')
        best_machine = None

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Machine load balancing heuristic:
            # Select machine with least current load among feasible machines.
            min_load = float('inf')
            candidate_machine = None
            candidate_time = None
            candidate_start_time = float('inf')

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                
                if machine_load[machine] < min_load:
                    min_load = machine_load[machine]
                    candidate_machine = machine
                    candidate_time = time
                    candidate_start_time = start_time
                elif machine_load[machine] == min_load and start_time < candidate_start_time:
                    candidate_machine = machine
                    candidate_time = time
                    candidate_start_time = start_time
            
            if candidate_machine is not None:
                processing_time = candidate_time
                earliest_start_time = candidate_start_time

                if earliest_start_time < best_start_time or (earliest_start_time == best_start_time and processing_time < best_processing_time):
                    best_start_time = earliest_start_time
                    best_processing_time = processing_time
                    best_op = op_data
                    best_machine = candidate_machine
                    best_time = candidate_time

        if best_op is not None:
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
            machine_load[best_machine] += best_time  # Update machine load
            job_completion_times[job_id] = end_time

            available_operations.remove(best_op)
            if op_idx + 1 < len(jobs[job_id]):
                available_operations.append({'job': job_id, 'op_idx': op_idx + 1})
        else:
             break # Break the loop in case no best operation

    return schedule
