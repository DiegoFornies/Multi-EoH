
def heuristic(input_data):
    """Heuristic for FJSSP: Minimizes makespan and balances machine load using a shortest processing time and least loaded machine strategy."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            # Find the machine with the shortest processing time and least load.
            best_machine, min_end_time = None, float('inf')
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_load[machine], job_completion_times[job])
                end_time = start_time + processing_time
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

            # Update schedule and machine load.
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_end_time,
                'Processing Time': best_processing_time
            })
            machine_load[best_machine] = min_end_time
            job_completion_times[job] = min_end_time

    return schedule
