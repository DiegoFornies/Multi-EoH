
def heuristic(input_data):
    """Schedules jobs balancing makespan and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    remaining_operations = {job: [(i + 1, op) for i, op in enumerate(jobs[job])] for job in range(1, n_jobs + 1)}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, ops in remaining_operations.items():
            if ops:
                eligible_operations.append((job, ops[0]))

        if not eligible_operations:
            break

        best_operation = None
        best_machine = None
        best_priority = float('inf')

        for job, (op_num, (machines, times)) in eligible_operations:
            for m_idx, m in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[m], job_completion_time[job])
                completion_time = start_time + processing_time
                
                priority = processing_time + 0.5 * machine_load[m] #Balance SPT and machine load.

                if priority < best_priority:
                    best_priority = priority
                    best_operation = (job, (op_num, (machines, times)))
                    best_machine = m
        
        if best_operation is not None and best_machine is not None:
            job, (op_num, (machines, times)) = best_operation
            m_idx = machines.index(best_machine)
            processing_time = times[m_idx]

            start_time = max(machine_available_time[best_machine], job_completion_time[job])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += processing_time
            job_completion_time[job] = end_time
            remaining_operations[job].pop(0)

    return schedule
