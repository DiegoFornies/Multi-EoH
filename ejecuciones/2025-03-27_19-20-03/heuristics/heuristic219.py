
def heuristic(input_data):
    """Schedules jobs using a global makespan and machine bottleneck resolution."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # 1. Estimate Machine Load
    machine_load = {m: 0 for m in range(n_machines)}
    for job in range(1, n_jobs + 1):
        for machines, times in jobs_data[job]:
            for m_idx, machine in enumerate(machines):
                machine_load[machine] += times[m_idx]

    # 2. Prioritize Machines with Highest Load
    sorted_machines = sorted(machine_load.items(), key=lambda item: item[1], reverse=True)
    prioritized_machines = [m for m, load in sorted_machines]

    # 3. Schedule jobs
    for job in range(1, n_jobs + 1):
        schedule[job] = []
        current_time = 0

        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1
            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None

            # Prioritize less loaded machines
            for machine in prioritized_machines:
                if machine in machines:
                    m_idx = machines.index(machine)
                    processing_time = times[m_idx]
                    start_time = max(machine_available_time[machine], current_time)

                    if start_time < min_start_time:
                        min_start_time = start_time
                        best_machine = machine
                        best_processing_time = processing_time
                        
            if best_machine is None:
                best_machine = machines[0] # Assign to first available machine
                best_processing_time = times[0]
                min_start_time = max(machine_available_time[best_machine], current_time)

            start_time = min_start_time
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
            current_time = end_time
            job_completion_time[job] = end_time

    return schedule
