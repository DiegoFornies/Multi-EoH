
def heuristic(input_data):
    """Hybrid heuristic: EFT with separation threshold."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_loads = {m: 0 for m in range(n_machines)}
    
    #Threshold for separation
    separation_threshold = 0.2 

    remaining_operations = {}
    for job_id, operations in jobs_data.items():
        remaining_operations[job_id] = list(range(1, len(operations) + 1))

    scheduled_operations_count = 0
    total_operations = sum(len(ops) for ops in jobs_data.values())

    while scheduled_operations_count < total_operations:
        eligible_operations = []
        for job_id, operations in jobs_data.items():
            if remaining_operations[job_id]:
                op_index = remaining_operations[job_id][0] - 1
                eligible_operations.append((job_id, op_index))
        
        best_operation = None
        best_machine = None
        earliest_start_time = float('inf')

        for job_id, op_index in eligible_operations:
            machines, times = jobs_data[job_id][op_index]
            
            best_machine_local = None
            earliest_start_time_local = float('inf')
            for m_index, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                if start_time < earliest_start_time_local:
                    earliest_start_time_local = start_time
                    best_machine_local = machine
                    processing_time = times[m_index]

            #Calculate load based separation.
            machine_load_normalized = machine_loads[best_machine_local]/sum(machine_loads.values()) if sum(machine_loads.values()) > 0 else 0
            
            if machine_load_normalized < separation_threshold:
                start_time = earliest_start_time_local
                if start_time < earliest_start_time:
                        earliest_start_time = start_time
                        best_operation = (job_id, op_index)
                        best_machine = best_machine_local
                        for m_index, machine in enumerate(machines):
                            if machine == best_machine:
                                processing_time = times[m_index]
                                break
            else: #Load balancing
                best_machine_local_load = None
                min_end_time_load = float('inf')
                for m_index, machine in enumerate(machines):
                    start_time = max(machine_available_time[machine], job_completion_time[job_id])
                    end_time = start_time + times[m_index]
                    machine_load_normalized = machine_loads[machine]/sum(machine_loads.values()) if sum(machine_loads.values()) > 0 else 0

                    if end_time < min_end_time_load:
                        min_end_time_load = end_time
                        best_machine_local_load = machine
                        processing_time_load = times[m_index]
                        start_time_load = start_time

                start_time = start_time_load
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_operation = (job_id, op_index)
                    best_machine = best_machine_local_load

                    processing_time = processing_time_load

        if best_operation is not None:
            job_id, op_index = best_operation
            machines, times = jobs_data[job_id][op_index]

            for m_index, machine in enumerate(machines):
                if machine == best_machine:
                    processing_time = times[m_index]
                    break

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            machine_loads[best_machine] += processing_time
            remaining_operations[job_id].pop(0)
            scheduled_operations_count += 1

    return schedule
