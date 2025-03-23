
def heuristic(input_data):
    """
    A heuristic for FJSSP that considers machine load and job precedence.
    It iterates through jobs and operations, assigning each operation to the machine
    that minimizes its completion time, considering both machine availability and
    job precedence.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Initialize job completion times

    for job_id, operations in jobs.items():
        schedule[job_id] = []
        for op_idx, operation in enumerate(operations):
            machines, processing_times = operation
            op_num = op_idx + 1

            best_machine = None
            min_completion_time = float('inf')
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = processing_times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                completion_time = start_time + processing_time

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
    return schedule
