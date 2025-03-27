
def heuristic(input_data):
    """Combines SPT, earliest machine, and load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    remaining_operations = {}
    for job in range(1, n_jobs + 1):
        remaining_operations[job] = [(i + 1, op) for i, op in enumerate(jobs_data[job])]

    job_priority = sorted(range(1, n_jobs + 1), key=lambda job_id: len(jobs_data[job_id]), reverse=True)

    while any(remaining_operations.values()):
        eligible_operations = []
        for job in job_priority:
            if remaining_operations[job]:
                eligible_operations.append((job, remaining_operations[job][0]))

        if not eligible_operations:
            break

        best_operation = None
        best_machine = None
        min_completion_time = float('inf')

        for job, (op_num, (machines, times)) in eligible_operations:
            shortest_time = float('inf')
            chosen_machine = None

            for m_idx, m in enumerate(machines):
                time = times[m_idx]
                start_time = max(machine_available_time[m], job_completion_time[job])
                completion_time = start_time + time
                
                #Prioritizing earliest machine + shortest processing time and machine load
                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_operation = (job, (op_num, (machines, times)))
                    best_machine = m
                    shortest_time = time

                elif completion_time == min_completion_time and machine_load[m] < machine_load[best_machine]:
                  best_operation = (job, (op_num, (machines, times)))
                  best_machine = m
                  shortest_time = time

        if best_operation is not None and best_machine is not None:
            job, (op_num, (machines, times)) = best_operation
            
            m_idx = machines.index(best_machine) if best_machine in machines else 0 
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
