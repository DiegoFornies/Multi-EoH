
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing idle time on machines
    and job completion time by considering machine availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        operations = jobs[job_id]

        for op_idx, op_data in enumerate(operations):
            machines, processing_times = op_data
            operation_number = op_idx + 1

            best_machine = None
            min_end_time = float('inf')

            # Find the best machine for the current operation
            for m_idx, machine in enumerate(machines):
                processing_time = processing_times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            # Assign the operation to the best machine
            schedule[job_id].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_end_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability and job completion time
            machine_available_time[best_machine] = min_end_time
            job_completion_time[job_id] = min_end_time

    return schedule
