
def heuristic(input_data):
    """Combines SPT priority and least-loaded machine for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_schedules = {m: [] for m in range(n_machines)}
    job_ops = {job: 0 for job in range(1, n_jobs + 1)}
    priority_queue = []

    for job in range(1, n_jobs + 1):
        ops = jobs_data[job]
        machines, times = ops[0]
        min_time = min(times)
        priority = min_time
        priority_queue.append((priority, job))

    priority_queue.sort()

    while priority_queue:
        priority, job = priority_queue.pop(0)

        if job not in schedule:
            schedule[job] = []

        op_idx = job_ops[job]
        machines, times = jobs_data[job][op_idx]

        best_machine = None
        min_load = float('inf')
        best_start_time = None
        best_processing_time = None

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_load[machine], job_completion_times[job])

            overlap = False
            for scheduled_op in machine_schedules[machine]:
                if start_time < scheduled_op['End Time'] and (start_time + processing_time) > scheduled_op['Start Time']:
                    overlap = True
                    break

            if not overlap:
                potential_load = machine_load[machine] + processing_time
                if potential_load < min_load:
                    min_load = potential_load
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        if best_machine is not None:
            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_schedules[best_machine].append({
                'Job': job,
                'Operation': op_idx + 1,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_load[best_machine] = best_start_time + best_processing_time
            job_completion_times[job] = best_start_time + best_processing_time
            job_ops[job] += 1

        else:
            m_idx = 0
            machine = machines[m_idx]
            processing_time = times[m_idx]

            start_time = max(machine_load[machine], job_completion_times[job])

            while True:
                overlap = False
                for scheduled_op in machine_schedules[machine]:
                    if start_time < scheduled_op['End Time'] and (start_time + processing_time) > scheduled_op['Start Time']:
                        start_time = scheduled_op['End Time']
                        overlap = True
                        break
                if not overlap:
                    break

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': start_time + processing_time,
                'Processing Time': processing_time
            })

            machine_schedules[machine].append({
                'Job': job,
                'Operation': op_idx + 1,
                'Start Time': start_time,
                'End Time': start_time + processing_time,
                'Processing Time': processing_time
            })
            machine_load[machine] = start_time + processing_time
            job_completion_times[job] = start_time + processing_time
            job_ops[job] += 1

        if job_ops[job] < len(jobs_data[job]):
            next_machines, next_times = jobs_data[job][job_ops[job]]
            min_time = min(next_times)
            priority = job_completion_times[job] + min_time
            priority_queue.append((priority, job))
            priority_queue.sort()

    return schedule
