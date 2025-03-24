
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP).
    Prioritizes operations with shorter processing times and considers machine availability
    to minimize makespan and balance machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 0))  # (job_id, operation_index)

    while eligible_operations:
        # Prioritize operations with shortest processing time among available machines.
        best_op = None
        min_end_time = float('inf')

        for job, op_idx in eligible_operations:
            machines, times = jobs_data[job][op_idx]
            
            # Find earliest possible end time for this operation
            earliest_start = float('-inf')
            chosen_machine = None
            chosen_time = None
            
            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + times[m_idx]

                if start_time > earliest_start:
                   earliest_start = start_time
                   chosen_machine = machine
                   chosen_time = times[m_idx]
                   earliest_end_time = end_time

            
            if earliest_end_time < min_end_time:
                min_end_time = earliest_end_time
                best_op = (job, op_idx, chosen_machine, earliest_start, chosen_time)

        job, op_idx, assigned_machine, start_time, processing_time = best_op
        operation_number = op_idx + 1
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': operation_number,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[assigned_machine] = end_time
        job_completion_time[job] = end_time

        # Update eligible operations
        eligible_operations.remove((job, op_idx))
        if op_idx + 1 < len(jobs_data[job]):
            eligible_operations.append((job, op_idx + 1))
            
    return schedule
