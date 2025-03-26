
def heuristic(input_data):
    """Combines load balancing & SPT for FJSSP."""
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {}

    for job_id in jobs:
        schedule[job_id] = []

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, machines, times))

    remaining_operations = {job_id: 1 for job_id in jobs}

    while operations:
        available_operations = []
        for idx, (job_id, op_num, machines, times) in enumerate(operations):
            if op_num == remaining_operations[job_id]:
                available_operations.append((idx, job_id, op_num, machines, times))

        if not available_operations:
            break

        best_op = None
        best_machine = None
        best_start_time = float('inf')
        best_idx = None
        best_processing_time = None

        for idx, (index_in_ops, job_id, op_num, machines, times) in enumerate(available_operations):
            last_op_end_time = job_completion_time[job_id]

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_time[machine], last_op_end_time)

                # Prioritize machine with earliest available time
                if start_time < best_start_time:
                    best_start_time = start_time
                    best_op = (job_id, op_num, machines, times)
                    best_machine = machine
                    best_processing_time = processing_time
                    best_idx = idx

        job_id, op_num, machines, times = best_op
        start_time = max(machine_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        operations.pop(index_to_remove)
        remaining_operations[job_id] += 1

    return schedule
