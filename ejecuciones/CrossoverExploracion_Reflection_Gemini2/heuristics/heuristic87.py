
def heuristic(input_data):
    """FJSSP heuristic: Combines SPT & machine load with few machines first."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    job_current_operation = {j: 0 for j in jobs_data}
    machine_load = {m: 0 for m in range(n_machines)}

    eligible_operations = []
    for job_id in jobs_data:
        machines, times = jobs_data[job_id][0]
        eligible_operations.append((job_id, 0, machines, times))
    
    scheduled_count = 0
    total_operations = sum(len(job) for job in jobs_data.values())

    while scheduled_count < total_operations:
        eligible_operations = []
        for job_id in jobs_data:
            if job_current_operation[job_id] < len(jobs_data[job_id]):
                op_idx = job_current_operation[job_id]
                machines, times = jobs_data[job_id][op_idx]
                eligible_operations.append((job_id, op_idx, machines, times))

        if not eligible_operations:
            break

        # Prioritize operations with fewest machine choices first.
        eligible_operations.sort(key=lambda x: len(x[2]))

        best_op = None
        best_machine = None
        min_end_time = float('inf')
        processing_time = 0

        for job_id, op_idx, machines, times in eligible_operations:
            #Find the best machine with SPT & machine load balance
            best_local_machine = None
            min_local_end_time = float('inf')
            local_processing_time = 0

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + times[m_idx]

                if end_time < min_local_end_time:
                    min_local_end_time = end_time
                    best_local_machine = machine
                    local_processing_time = times[m_idx]

            start_time = max(machine_available_time[best_local_machine], job_completion_time[job_id])

            if start_time + local_processing_time < min_end_time:
                min_end_time = start_time + local_processing_time
                best_op = (job_id, op_idx, machines, times)
                best_machine = best_local_machine
                processing_time = local_processing_time

        if best_op is None:
            break

        job_id, op_idx, machines, times = best_op
        op_num = op_idx + 1

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        machine_load[best_machine] += processing_time

        job_current_operation[job_id] += 1
        scheduled_count +=1

    return schedule
