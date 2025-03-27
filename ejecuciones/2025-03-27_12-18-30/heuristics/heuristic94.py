
def heuristic(input_data):
    """Combines SPT, earliest start, and load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    machine_load = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    remaining_operations = {}
    for job in range(1, n_jobs + 1):
        remaining_operations[job] = [(i + 1, op) for i, op in enumerate(jobs_data[job])]

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, ops in remaining_operations.items():
            if ops:
                eligible_operations.append((job, ops[0]))

        best_operation = None
        best_machine = None
        min_end_time = float('inf')

        for job, (op_num, (machines, times)) in eligible_operations:
            best_local_machine = None
            shortest_time = float('inf')
            
            for m_idx, m in enumerate(machines):
                time = times[m_idx]
                if time < shortest_time:
                    shortest_time = time
                    best_local_machine = m

            if best_local_machine is not None:
                start_time = max(machine_available_time[best_local_machine], job_completion_time[job])
                end_time = start_time + shortest_time
                load_factor = machine_load[best_local_machine]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_operation = (job, (op_num, (machines, times)))
                    best_machine = best_local_machine
                elif end_time == min_end_time and load_factor < machine_load.get(best_machine, float('inf')): #Prioritize the min end time and load balancing
                    best_operation = (job, (op_num, (machines, times)))
                    best_machine = best_local_machine

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
            machine_load[best_machine] += processing_time #update machine load
            job_completion_time[job] = end_time
            remaining_operations[job].pop(0)

    return schedule
