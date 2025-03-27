
def heuristic(input_data):
    """Prioritizes operations with fewer machine choices to reduce bottlenecks."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    remaining_operations = {job: [(i + 1, op) for i, op in enumerate(jobs_data[job])] for job in range(1, n_jobs + 1)}

    while any(remaining_operations.values()):
        eligible_operations = [(job, op) for job, ops in remaining_operations.items() if ops]

        # Prioritize operations with the fewest machine choices
        eligible_operations.sort(key=lambda x: len(x[1][1][0]))

        best_operation = None
        best_machine = None
        min_end_time = float('inf')

        for job, (op_num, (machines, times)) in eligible_operations:
            best_start_time_local = float('inf')
            best_machine_local = None
            best_processing_time_local = None

            for i, machine in enumerate(machines):
                start_time = max(machine_time[machine], job_completion_time[job])
                processing_time = times[i]
                end_time = start_time + processing_time

                if end_time < best_start_time_local + best_processing_time_local:
                    best_start_time_local = start_time
                    best_machine_local = machine
                    best_processing_time_local = processing_time

            if best_machine_local is not None and best_start_time_local + best_processing_time_local < min_end_time:
                min_end_time = best_start_time_local + best_processing_time_local
                best_operation = (job, (op_num, (machines, times)))
                best_machine = best_machine_local

        if best_operation is not None and best_machine is not None:
            job, (op_num, (machines, times)) = best_operation
            m_idx = machines.index(best_machine)
            processing_time = times[m_idx]
            start_time = max(machine_time[best_machine], job_completion_time[job])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_time[best_machine] = end_time
            job_completion_time[job] = end_time
            remaining_operations[job].pop(0)

    return schedule
