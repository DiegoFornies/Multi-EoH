
def heuristic(input_data):
    """
    Heuristic for FJSSP, balances makespan, idle time, and machine load using dynamic weighting.
    Prioritizes operations based on a weighted sum of factors.
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
        for job_id, op_index in [(j, op - 1) for j in jobs_data for op in (remaining_operations.get(j) or [])[:1]]: # iterate only first op

            machines, times = jobs_data[job_id][op_index]
            for m_index, machine in enumerate(machines):
                eligible_operations.append((job_id, op_index, machine, times[m_index]))

        if not eligible_operations:
            break # Handle potential deadlocks

        # Dynamic Weighting
        makespan_weight = 0.4
        idle_time_weight = 0.3
        load_balance_weight = 0.3

        best_operation = None
        best_machine = None
        best_score = float('inf')

        for job_id, op_index, machine, processing_time in eligible_operations:
            start_time = max(machine_available_time[machine], job_completion_time[job_id])

            # Calculate factors for the weighted score
            makespan_factor = start_time + processing_time
            idle_time_factor = machine_available_time[machine] - job_completion_time[job_id] if machine_available_time[machine] > job_completion_time[job_id] else 0
            load_balance_factor = machine_loads[machine]

            # Calculate weighted score
            score = (makespan_weight * makespan_factor +
                     idle_time_weight * idle_time_factor +
                     load_balance_weight * load_balance_factor)

            if score < best_score:
                best_score = score
                best_operation = (job_id, op_index)
                best_machine = machine
                best_processing_time = processing_time

        if best_operation is not None:
            job_id, op_index = best_operation
            processing_time = best_processing_time
            best_machine = best_machine
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
