
def heuristic(input_data):
    """Combines SPT and load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    remaining_operations = {job: [(i + 1, op) for i, op in enumerate(jobs[job])] for job in range(1, n_jobs + 1)}

    while any(remaining_operations.values()):
        eligible_operations = [(job, ops[0]) for job, ops in remaining_operations.items() if ops]

        best_operation = None
        best_machine = None
        min_completion_time = float('inf')

        for job, (op_num, (machines, times)) in eligible_operations:
            shortest_time = float('inf')
            chosen_machine = None
            min_load = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                completion_time = start_time + processing_time

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    chosen_machine = machine
                    shortest_time = processing_time
                    best_start_time = start_time
                    min_load = machine_available_time[machine]
                elif completion_time == min_completion_time and machine_available_time[machine] < min_load:
                    chosen_machine = machine
                    shortest_time = processing_time
                    best_start_time = start_time
                    min_load = machine_available_time[machine]

            if chosen_machine is not None:
                best_operation = (job, (op_num, (machines, times)))
                best_machine = chosen_machine
                processing_time = shortest_time
                start_time = best_start_time
                end_time = start_time + processing_time
                
                
                
        if best_operation is not None and best_machine is not None:
            job, (op_num, (machines, times)) = best_operation
            start_time = max(machine_available_time[best_machine], job_completion_time[job])
            m_idx = machines.index(best_machine) if best_machine in machines else 0 
            processing_time = times[m_idx] 
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time
            remaining_operations[job].pop(0)

    return schedule
