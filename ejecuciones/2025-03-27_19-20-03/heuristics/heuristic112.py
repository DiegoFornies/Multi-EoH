
def heuristic(input_data):
    """Combines SPT job order and least loaded machine selection to minimize makespan."""
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

    job_order = sorted(job_remaining_times.keys(), key=job_remaining_times.get)

    for job in job_order:
        schedule[job] = []
        current_job_completion = 0

        for op_idx, operation in enumerate(jobs_data[job]):
            machines, times = operation

            best_machine = None
            min_completion_time = float('inf')
            best_start_time = None
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_load[machine], current_job_completion)

                overlap = False
                for scheduled_op in machine_schedules[machine]:
                    if start_time < scheduled_op['End Time'] and (start_time + processing_time) > scheduled_op['Start Time']:
                        overlap = True
                        break

                if not overlap:
                    completion_time = start_time + processing_time
                    if completion_time < min_completion_time:
                        min_completion_time = completion_time
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
                current_job_completion = best_start_time + best_processing_time
                job_completion_times[job] = current_job_completion
            else:
                # If no machine is available, choose one with minimal delay.
                machine_delays = {}
                for m_idx, machine in enumerate(machines):
                    processing_time = times[m_idx]
                    start_time = max(machine_load[machine], current_job_completion)
                    overlap = False
                    for scheduled_op in machine_schedules[machine]:
                        if start_time < scheduled_op['End Time'] and (start_time + processing_time) > scheduled_op['Start Time']:
                            overlap = True
                            break
                    if overlap:
                        # Find the first available slot on this machine
                        last_end_time = 0
                        for scheduled_op in sorted(machine_schedules[machine], key = lambda x: x['Start Time']):
                            if current_job_completion >= scheduled_op['End Time']:
                                last_end_time = scheduled_op['End Time']
                                continue
                            
                            if current_job_completion < scheduled_op['Start Time']:
                                machine_delays[machine] = scheduled_op['Start Time'] - current_job_completion
                                break

                            
                        if machine not in machine_delays:
                            machine_delays[machine] = float('inf')
                    else:
                        machine_delays[machine] = max(0, machine_load[machine] - current_job_completion)

                
                best_machine = min(machine_delays, key=machine_delays.get)
                m_idx = machines.index(best_machine)
                processing_time = times[m_idx]
                start_time = max(machine_load[best_machine], current_job_completion)

                # Ensure no overlap.
                while True:
                    overlap = False
                    for scheduled_op in machine_schedules[best_machine]:
                        if start_time < scheduled_op['End Time'] and (start_time + processing_time) > scheduled_op['Start Time']:
                            start_time = scheduled_op['End Time']
                            overlap = True
                            break
                    if not overlap:
                        break

                schedule[job].append({
                    'Operation': op_idx + 1,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': start_time + processing_time,
                    'Processing Time': processing_time
                })

                machine_schedules[best_machine].append({
                    'Job': job,
                    'Operation': op_idx + 1,
                    'Start Time': start_time,
                    'End Time': start_time + processing_time,
                    'Processing Time': processing_time
                })
                machine_load[best_machine] = start_time + processing_time
                current_job_completion = start_time + processing_time
                job_completion_times[job] = current_job_completion

    return schedule
