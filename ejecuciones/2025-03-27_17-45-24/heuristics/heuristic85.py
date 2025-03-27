
def heuristic(input_data):
    """Hybrid heuristic for FJSSP: EFT and load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    remaining_operations = {}
    for job_id, operations in jobs.items():
        remaining_operations[job_id] = list(range(1, len(operations) + 1))

    scheduled_operations_count = 0
    total_operations = sum(len(ops) for ops in jobs.values())

    while scheduled_operations_count < total_operations:
        eligible_operations = []
        for job_id, operations in jobs.items():
            if remaining_operations[job_id]:
                op_index = remaining_operations[job_id][0] - 1
                eligible_operations.append((job_id, op_index))

        best_operation = None
        best_machine = None
        earliest_start_time = float('inf')

        for job_id, op_index in eligible_operations:
            machines, times = jobs[job_id][op_index]
            for m_index, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                finish_time = start_time + times[m_index]

                # Load balancing consideration: prefer lightly loaded machine
                load_factor = 1.0 + (machine_load[machine] / sum(machine_load.values()) if sum(machine_load.values()) > 0 else 0)
                adjusted_start_time = start_time * load_factor
                if adjusted_start_time < earliest_start_time:
                    earliest_start_time = adjusted_start_time
                    best_operation = (job_id, op_index)
                    best_machine = machine
                    processing_time = times[m_index]

        if best_operation is not None:
            job_id, op_index = best_operation
            machines, times = jobs[job_id][op_index]

            for m_index, machine in enumerate(machines):
                if machine == best_machine:
                    processing_time = times[m_index]
                    break

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            machine_load[best_machine] += processing_time

            remaining_operations[job_id].pop(0)
            scheduled_operations_count += 1

    return schedule
