
def heuristic(input_data):
    """Schedules jobs using a separation-aware balancing approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    remaining_operations = {job: list(range(1, len(ops) + 1)) for job, ops in jobs_data.items()}

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, operations in remaining_operations.items():
            if operations:
                op_num = operations[0]
                machines, times = jobs_data[job][op_num - 1]
                eligible_operations.append((job, op_num, machines, times, job))

        best_op = None
        best_machine = None
        min_cost = float('inf')
        best_job = None
        best_processing_time = None

        for job, op_num, machines, times, _ in eligible_operations:
            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])
                processing_time = times[m_idx]
                end_time = start_time + processing_time
                
                # Separation-Aware Balancing: Prioritize low load + separation from same job on machine
                cost = end_time + machine_available_time[machine] # makespan + machine load

                if cost < min_cost:
                    min_cost = cost
                    best_op = op_num
                    best_machine = machine
                    best_job = job
                    best_processing_time = processing_time

        if best_job not in schedule:
            schedule[best_job] = []

        start_time = max(machine_available_time[best_machine], job_completion_time[best_job])
        end_time = start_time + best_processing_time

        schedule[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[best_job] = end_time
        remaining_operations[best_job].pop(0)

    return schedule
