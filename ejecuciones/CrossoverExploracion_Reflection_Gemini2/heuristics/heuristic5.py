
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing idle time on machines
    and balances machine load by selecting the machine with the earliest
    available time for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in jobs:
        schedule[job_id] = []
        ops = jobs[job_id]

        for op_idx, operation in enumerate(ops):
            machines, processing_times = operation
            op_num = op_idx + 1

            best_machine = None
            min_end_time = float('inf')

            for i, machine in enumerate(machines):
                processing_time = processing_times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = min_end_time
            job_completion_time[job_id] = min_end_time

    return schedule
