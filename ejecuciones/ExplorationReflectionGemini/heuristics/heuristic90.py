
def heuristic(input_data):
    """FJSSP heuristic: Shortest processing time, earliest machine available."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    unassigned_operations = []

    for job_id, operations in jobs_data.items():
        for op_idx, op_data in enumerate(operations):
            unassigned_operations.append({
                'job': job_id,
                'operation': op_idx + 1,
                'machines': op_data[0],
                'times': op_data[1]
            })

    while unassigned_operations:
        best_operation = None
        earliest_end_time = float('inf')

        for op in unassigned_operations:
            job_id = op['job']
            machines = op['machines']
            times = op['times']
            op_idx = op['operation']

            if not schedule[job_id]:
                if op_idx != 1:
                    continue
            else:
                last_scheduled_op = schedule[job_id][-1]['Operation']
                if op_idx != last_scheduled_op + 1:
                    continue

            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + times[i]

                if end_time < earliest_end_time:
                    earliest_end_time = end_time
                    best_operation = op
                    best_machine = machine
                    best_time = times[i]

        if best_operation is None:
            return "Infeasible solution"

        job_id = best_operation['job']
        op_num = best_operation['operation']
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        unassigned_operations.remove(best_operation)

    return schedule
