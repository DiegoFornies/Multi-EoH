
def heuristic(input_data):
    """Combines earliest start time with load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    remaining_operations = {}
    for job_id, operations in jobs_data.items():
        remaining_operations[job_id] = list(range(1, len(operations) + 1))

    scheduled_operations_count = 0
    total_operations = sum(len(ops) for ops in jobs_data.values())

    while scheduled_operations_count < total_operations:
        eligible_operations = []
        for job_id, operations in jobs_data.items():
            if remaining_operations[job_id]:
                op_index = remaining_operations[job_id][0] - 1
                eligible_operations.append((job_id, op_index))

        best_operation = None
        best_machine = None
        earliest_adjusted_end_time = float('inf')

        for job_id, op_index in eligible_operations:
            machines, times = jobs_data[job_id][op_index]
            for m_index, machine in enumerate(machines):
                processing_time = times[m_index]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time
                load_factor = 1 + machine_load[machine] / (sum(machine_load.values()) + 1e-9)
                adjusted_end_time = end_time * load_factor

                if adjusted_end_time < earliest_adjusted_end_time:
                    earliest_adjusted_end_time = adjusted_end_time
                    best_operation = (job_id, op_index)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        if best_operation is not None:
            job_id, op_index = best_operation
            start_time = best_start_time
            processing_time = best_processing_time
            end_time = start_time + processing_time
            machine = best_machine
            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = end_time
            job_completion_time[job_id] = end_time
            machine_load[machine] += processing_time
            remaining_operations[job_id].pop(0)
            scheduled_operations_count += 1

    return schedule
