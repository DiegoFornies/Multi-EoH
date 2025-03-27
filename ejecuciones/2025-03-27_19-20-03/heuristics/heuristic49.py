
def heuristic(input_data):
    """Prioritizes jobs with most operations, assigns to earliest available machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_schedules = {m: [] for m in range(n_machines)}

    # Prioritize jobs with the most operations
    job_priority = {job: len(operations) for job, operations in jobs_data.items()}
    job_order = sorted(job_priority.keys(), key=job_priority.get, reverse=True)

    for job in job_order:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs_data[job]):
            machines, times = operation

            best_machine = None
            earliest_start_time = float('inf')
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
                    if start_time < earliest_start_time:
                        earliest_start_time = start_time
                        best_machine = machine
                        best_processing_time = processing_time

            if best_machine is not None:
                schedule[job].append({
                    'Operation': op_idx + 1,
                    'Assigned Machine': best_machine,
                    'Start Time': earliest_start_time,
                    'End Time': earliest_start_time + best_processing_time,
                    'Processing Time': best_processing_time
                })

                machine_schedules[best_machine].append({
                    'Job': job,
                    'Operation': op_idx + 1,
                    'Start Time': earliest_start_time,
                    'End Time': earliest_start_time + best_processing_time,
                    'Processing Time': best_processing_time
                })
                machine_load[best_machine] = earliest_start_time + best_processing_time
                job_completion_times[job] = earliest_start_time + best_processing_time
            else:
                # Fallback: if no feasible machine is found assign to first avail
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

    return schedule
