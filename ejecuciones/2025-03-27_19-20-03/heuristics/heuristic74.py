
def heuristic(input_data):
    """Schedules jobs using a Least Work Remaining (LWR) rule."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_remaining_work = {}

    for job, operations in jobs_data.items():
        job_remaining_work[job] = sum(min(times) for machines, times in operations)

    job_order = sorted(job_remaining_work.keys(), key=job_remaining_work.get)

    for job in job_order:
        schedule[job] = []
        current_time = 0
        last_end_time = 0

        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1
            best_machine, best_time, best_processing_time = None, float('inf'), None
            
            available_machines = []
            available_times = []
            available_processing_times = []

            for m_idx, machine in enumerate(machines):
                 available_machines.append(machine)
                 available_times.append(machine_available_time[machine])
                 available_processing_times.append(times[m_idx])

            # First available machine
            best_machine_index = available_times.index(min(available_times))
            best_machine = available_machines[best_machine_index]
            best_time = available_times[best_machine_index]
            best_processing_time = available_processing_times[best_machine_index]


            start_time = max(best_time, last_end_time)
            processing_time = best_processing_time
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            last_end_time = end_time
            job_completion_time[job] = end_time
            job_remaining_work[job] -= processing_time

    return schedule
