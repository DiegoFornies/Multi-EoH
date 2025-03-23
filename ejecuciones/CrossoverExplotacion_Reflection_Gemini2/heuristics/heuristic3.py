
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing idle time by
    assigning operations to the earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in jobs_data:
        schedule[job_id] = []
        operations = jobs_data[job_id]

        for op_idx, op_data in enumerate(operations):
            machines = op_data[0]
            times = op_data[1]

            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            if best_machine is not None:
                start_time = min_start_time
                end_time = start_time + best_processing_time

                schedule[job_id].append({
                    'Operation': op_idx + 1,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': best_processing_time
                })

                machine_available_time[best_machine] = end_time
                job_completion_time[job_id] = end_time

    return schedule
