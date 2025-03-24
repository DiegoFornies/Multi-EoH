
def heuristic(input_data):
    """
    Schedules operations based on earliest finish time and machine load.
    Minimizes makespan and balances machine utilization.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    schedule = {}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, operation in enumerate(jobs_data[job]):
            op_num = op_idx + 1
            available_machines, processing_times = operation

            # Prioritize machines with lower load
            available_machines_load = [(machine, machine_load[machine]) for machine in available_machines]
            available_machines_load.sort(key=lambda x: x[1])

            best_machine = None
            min_end_time = float('inf')

            for machine_data in available_machines_load:
                machine = machine_data[0]

                machine_idx = available_machines.index(machine) # ensure the index matches correctly
                processing_time = processing_times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            
    return schedule
