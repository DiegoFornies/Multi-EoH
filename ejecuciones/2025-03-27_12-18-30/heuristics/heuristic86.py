
def heuristic(input_data):
    """Combines SPT and earliest machine with dynamic job prioritization."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    remaining_operations = {}

    for job in range(1, n_jobs + 1):
        remaining_operations[job] = [(i + 1, op) for i, op in enumerate(jobs_data[job])]

    scheduled_operations = []
    job_priority = {job: len(ops) for job, ops in remaining_operations.items()} # Prioritize jobs with more remaining operations

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, ops in remaining_operations.items():
            if ops:
                eligible_operations.append((job, ops[0]))  # (job, (op_num, (machines, times)))
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
                if time < shortest_time:
                    shortest_time = time
                    chosen_machine = m

            if chosen_machine is not None:
                start_time = max(machine_available_time[chosen_machine], job_completion_time[job])
                completion_time = start_time + shortest_time

                # Adjust completion time based on job priority. Higher priority = lower completion time
                adjusted_completion_time = completion_time - (job_priority[job] * 0.01)

                if adjusted_completion_time < min_completion_time:
                    min_completion_time = adjusted_completion_time
                    best_operation = (job, (op_num, (machines, times)))
                    best_machine = chosen_machine

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
            job_completion_time[job] = end_time
            remaining_operations[job].pop(0)
            job_priority[job] = len(remaining_operations[job]) # Update Job remaining count

    return schedule
