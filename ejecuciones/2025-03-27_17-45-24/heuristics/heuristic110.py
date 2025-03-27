
def heuristic(input_data):
    """
    Schedules jobs considering machine load and earliest finish time.
    Dynamically adjusts priority between load balancing and EFT.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_loads = {m: 0 for m in range(n_machines)}

    schedule = {j: [] for j in range(1, n_jobs + 1)}
    
    remaining_operations = {}
    for job_id, operations in jobs_data.items():
        remaining_operations[job_id] = list(range(1, len(operations) + 1)) 

    scheduled_operations_count = 0
    total_operations = sum(len(ops) for ops in jobs_data.values())

    while scheduled_operations_count < total_operations:
        eligible_operations = []
        for job_id, op_index in jobs_data.items():
            if remaining_operations[job_id]:
                op_index_internal = remaining_operations[job_id][0] - 1
                eligible_operations.append((job_id, op_index_internal))

        best_operation = None
        best_machine = None
        earliest_finish_time = float('inf')
        
        #Adaptive weight for machine load vs EFT
        load_weight = 0.5  # Adjust dynamically based on problem characteristics

        for job_id, op_index in eligible_operations:
            machines, times = jobs_data[job_id][op_index]
            for m_index, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                processing_time = times[m_index]
                finish_time = start_time + processing_time
                
                # Calculate a score considering both finish time and machine load
                load_score = machine_loads[machine] / (sum(machine_loads.values()) + 1e-6) # Avoid division by zero
                score = (1 - load_weight) * finish_time + load_weight * load_score

                if score < earliest_finish_time:
                    earliest_finish_time = score
                    best_operation = (job_id, op_index)
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time
                    

        if best_operation is not None:
            job_id, op_index = best_operation
            
            start_time = best_start_time
            end_time = start_time + best_processing_time
        
            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            machine_loads[best_machine] += best_processing_time

            remaining_operations[job_id].pop(0)
            scheduled_operations_count += 1

    return schedule
