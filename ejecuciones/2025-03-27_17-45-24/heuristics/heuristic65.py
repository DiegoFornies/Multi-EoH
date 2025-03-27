
def heuristic(input_data):
    """Schedules FJSSP minimizing makespan by prioritizing critical operations."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    schedule = {j: [] for j in range(1, n_jobs + 1)}
    remaining_operations = {j: list(range(1, len(ops) + 1)) for j, ops in jobs_data.items()}
    
    scheduled_operations_count = 0
    total_operations = sum(len(ops) for ops in jobs_data.values())

    while scheduled_operations_count < total_operations:
        eligible_operations = []
        for job_id, operations in jobs_data.items():
            if remaining_operations[job_id]:
                op_index = remaining_operations[job_id][0] - 1
                eligible_operations.append((job_id, op_index, job_id)) # Include job_id for tie-breaking

        # Prioritize operations based on remaining work in the job
        eligible_operations.sort(key=lambda x: len(remaining_operations[x[2]]))

        best_operation = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, op_index, _ in eligible_operations:
            machines, times = jobs_data[job_id][op_index]
            for m_index, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + times[m_index]
                
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_operation = (job_id, op_index)
                    best_machine = machine
                    best_processing_time = times[m_index] # Store processing time
                    
        if best_operation:
            job_id, op_index = best_operation
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
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
            remaining_operations[job_id].pop(0)
            scheduled_operations_count += 1

    return schedule
