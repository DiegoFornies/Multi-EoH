
def heuristic(input_data):
    """LPT job order, least loaded machine, insertion-based scheduling."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_schedules = {m: [] for m in range(n_machines)}

    job_remaining_times = {}
    for job, operations in jobs_data.items():
        total_time = sum(min(times) for machines, times in operations)
        job_remaining_times[job] = total_time

    job_order = sorted(job_remaining_times.keys(), key=job_remaining_times.get, reverse=True)

    for job in job_order:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs_data[job]):
            machines, times = operation

            best_machine = None
            best_start_time = None
            best_processing_time = None
            min_end_time = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                
                # Iterate through possible start times to find the best insertion point
                start_time = max(machine_load[machine], job_completion_times[job])

                # Check for overlapping with existing scheduled operations on the machine
                while True:
                    overlap = False
                    for scheduled_op in machine_schedules[machine]:
                        if start_time < scheduled_op['End Time'] and (start_time + processing_time) > scheduled_op['Start Time']:
                            start_time = scheduled_op['End Time']  # Shift start time if overlap
                            overlap = True
                            break
                    if not overlap:
                        break

                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

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
            machine_load[best_machine] = max(machine_load[best_machine],best_start_time + best_processing_time)
            job_completion_times[job] = max(job_completion_times[job], best_start_time + best_processing_time)
            # Sort operations on machines by start time
            machine_schedules[best_machine].sort(key=lambda x: x['Start Time'])

    return schedule
