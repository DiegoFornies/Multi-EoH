
def heuristic(input_data):
    """Combines SPT, machine load, and job sequencing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    available_operations = []
    for job_id in jobs_data:
        available_operations.append((job_id, 1))  # (job_id, operation_number)

    while available_operations:
        best_op = None
        min_combined_score = float('inf')

        for job_id, op_num in available_operations:
            machines, times = jobs_data[job_id][op_num - 1]

            best_machine = -1
            best_start_time = float('inf')
            best_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                end_time = start_time + time

                idle_time = start_time - machine_available_time[machine] if start_time > machine_available_time[machine] else 0
                combined_score = end_time + 0.05 * machine_load[machine] - 0.02 * idle_time  # SPT + load balance

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_machine = machine
                    best_start_time = start_time
                    best_time = time
                    best_op = (job_id, op_num, machine, start_time, time)

        if best_op is not None:
            job_id, op_num, machine, start_time, time = best_op
            end_time = start_time + time

            if job_id not in schedule:
                schedule[job_id] = []

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': time
            })

            machine_available_time[machine] = end_time
            job_last_end_time[job_id] = end_time
            machine_load[machine] += time

            available_operations.remove((job_id, op_num))
            if op_num < len(jobs_data[job_id]):
                available_operations.append((job_id, op_num + 1))

        else:
            break # handle corner cases where no eligible operations can be chosen

    return schedule
