
def heuristic(input_data):
    """Schedule using shortest processing time on least loaded machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        current_time = 0

        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1
            best_machine = None
            min_processing_time = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]

                if processing_time < min_processing_time:
                    min_processing_time = processing_time
                    best_machine = machine
                    best_time = processing_time

                elif processing_time == min_processing_time and \
                        machine_load[machine] < (machine_load[best_machine] if best_machine is not None else float('inf')):
                    best_machine = machine
                    best_time = processing_time
            if best_machine is None:
                best_machine = machines[0]
                best_time = times[0]

            start_time = max(machine_time[best_machine], job_completion_time[job])
            end_time = start_time + best_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            machine_time[best_machine] = end_time
            machine_load[best_machine] += best_time
            current_time = end_time
            job_completion_time[job] = end_time

    return schedule
