
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing idle time on machines.
    It iteratively assigns operations to the machine that can process it earliest,
    considering both machine availability and job sequence.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}  # Corrected job range

    for job_id in range(1, n_jobs + 1):  # Corrected job range
        schedule[job_id] = []
        job_operations = jobs_data[job_id]

        for op_idx, operation in enumerate(job_operations):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_start_time = float('inf')
            processing_time = None

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    processing_time = times[m_idx]

            start_time = min_start_time
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            job_last_end_time[job_id] = end_time

    return schedule
