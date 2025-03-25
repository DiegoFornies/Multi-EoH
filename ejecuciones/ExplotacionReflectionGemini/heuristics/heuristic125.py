
def heuristic(input_data):
    """Combines machine load and job order for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    solution = {}
    for job_id in jobs:
        solution[job_id] = []

    eligible_operations = []
    for job_id, operations in jobs.items():
        for op_idx, op_data in enumerate(operations):
            eligible_operations.append((job_id, op_idx, op_data[0], op_data[1]))

    scheduled_operations = set()

    while len(scheduled_operations) < sum(len(ops) for ops in jobs.values()):

        best_operation = None
        best_machine = None
        min_end_time = float('inf')
        best_processing_time = None
        best_start_time = None

        for job_id, op_idx, machines, times in eligible_operations:
            if (job_id, op_idx) in scheduled_operations:
                continue

            preceding_operations_scheduled = True
            for prev_op_idx in range(op_idx):
                if (job_id, prev_op_idx) not in scheduled_operations:
                    preceding_operations_scheduled = False
                    break

            if not preceding_operations_scheduled:
                continue

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]

                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time
                    best_operation = (job_id, op_idx, machines, times)
                    best_start_time = start_time

        if best_operation:
            job_id, op_idx, machines, times = best_operation
            op_num = op_idx + 1
            end_time = best_start_time + best_processing_time

            solution[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time
            scheduled_operations.add((job_id, op_idx))

    return solution
