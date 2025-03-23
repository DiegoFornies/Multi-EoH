
def heuristic(input_data):
    """Schedules jobs using a combined greedy heuristic."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, machines, times))

    operations.sort(key=lambda x: min(x[3]))

    while operations:
        best_op, best_machine, best_start_time, best_processing_time = None, None, float('inf'), None
        best_op_index = None

        for i in range(len(operations)):
            job_id, op_num, machines, times = operations[i]

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

            for j in range(len(machines)):
                machine = machines[j]
                time = times[j]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                if start_time < earliest_start or (start_time == earliest_start and time < selected_time):
                    earliest_start = start_time
                    selected_machine = machine
                    selected_time = time

            if selected_machine is not None:
              if best_start_time > earliest_start:
                best_op = (job_id, op_num, machines, times)
                best_machine = selected_machine
                best_start_time = earliest_start
                best_processing_time = selected_time
                best_op_index = i

        if best_op is None:
            break

        job_id, op_num, machines, times = best_op
        start_time = best_start_time
        end_time = start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

        operations.pop(best_op_index)

    return schedule
