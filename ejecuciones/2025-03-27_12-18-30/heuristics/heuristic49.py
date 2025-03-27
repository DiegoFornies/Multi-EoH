
def heuristic(input_data):
    """
    Schedules jobs using a hybrid approach: earliest start time with machine load balancing.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        job_completion_time = 0

        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            best_machine = None
            earliest_start_time = float('inf')
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time)

                # Prioritize earliest start time, then balance machine load.
                load_factor = machine_load[machine]  # Simple load factor
                if start_time < earliest_start_time :
                    earliest_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
                elif start_time == earliest_start_time and load_factor < machine_load.get(best_machine,0):
                    best_machine = machine
                    best_processing_time = processing_time


            start_time = max(machine_available_time[best_machine], job_completion_time)
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += best_processing_time
            job_completion_time = end_time

    return schedule
