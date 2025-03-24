
def heuristic(input_data):
    """
    Hybrid heuristic for FJSSP: Shortest Remaining Processing Time and earliest start time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    remaining_times = {}
    for job_id, job in jobs_data.items():
        remaining_times[job_id] = sum(min(times) for machines, times in job)

    job_current_operation = {j: 0 for j in jobs_data}
    scheduled_operations = set()

    while len(scheduled_operations) < sum(len(ops) for ops in jobs_data.values()):
        eligible_operations = []
        for job_id in jobs_data:
            op_idx = job_current_operation[job_id]
            if op_idx >= len(jobs_data[job_id]):
                continue

            machines, times = jobs_data[job_id][op_idx]
            eligible_operations.append((job_id, op_idx, machines, times))

        if not eligible_operations:
            break

        #Sort by Shortest Remaining Processing Time first
        eligible_operations.sort(key=lambda x: remaining_times[x[0]])

        best_op = None
        best_machine = None
        earliest_start = float('inf')
        processing_time = 0

        for job_id, op_idx, machines, times in eligible_operations:
            for m_idx, machine in enumerate(machines):
                available_time = machine_available_time[machine]
                start_time = max(available_time, job_completion_time[job_id])
                end_time = start_time + times[m_idx]

                if start_time < earliest_start:
                    earliest_start = start_time
                    best_op = (job_id, op_idx, machines, times)
                    best_machine = machine
                    processing_time = times[m_idx]

        if best_op is None:
            break

        job_id, op_idx, machines, times = best_op
        op_num = op_idx + 1

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        scheduled_operations.add((job_id, op_idx))
        remaining_times[job_id] -= processing_time
        job_current_operation[job_id] += 1

    return schedule
