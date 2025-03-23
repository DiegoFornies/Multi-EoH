
def heuristic(input_data):
    """Combines sorting operations and earliest finish time for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, operation in enumerate(jobs_data[job_id]):
            operations.append((job_id, op_idx + 1, operation[0], operation[1]))

    operations.sort(key=lambda x: min(x[3]))

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    while operations:
        best_op, best_machine, best_start_time, best_processing_time = None, None, float('inf'), None
        best_op_index = None

        for i in range(len(operations)):
            job_id, op_num, machines, processing_times = operations[i]

            can_schedule = True
            if op_num > 1:
                prev_op_num = op_num - 1
                prev_scheduled = False
                for scheduled_op in schedule[job_id]:
                    if scheduled_op['Operation'] == prev_op_num:
                        prev_scheduled = True
                        break
                if not prev_scheduled:
                    can_schedule = False

            if not can_schedule:
                continue

            earliest_start = float('inf')
            selected_machine = None
            selected_time = None

            for j, machine in enumerate(machines):
                processing_time = processing_times[j]
                start_time = max(machine_available[machine], job_completion[job_id])
                end_time = start_time + processing_time
                if end_time < earliest_start:
                    earliest_start = start_time
                    selected_machine = machine
                    selected_time = processing_time
            
            if selected_machine is not None:
                if earliest_start < best_start_time:
                    best_op = (job_id, op_num, machines, processing_times)
                    best_machine = selected_machine
                    best_start_time = earliest_start
                    best_processing_time = selected_time
                    best_op_index = i

        if best_op is None:
            break

        job_id, op_num, machines, processing_times = best_op
        start_time = best_start_time
        end_time = start_time + best_processing_time
        best_machine = best_machine

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available[best_machine] = end_time
        job_completion[job_id] = end_time
        operations.pop(best_op_index)

    return schedule
