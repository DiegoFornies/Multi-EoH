
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes shortest processing time
    and earliest machine availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_num in range(1, n_jobs + 1):
        schedule[job_num] = []
        operations = jobs[job_num]

        for op_idx, operation in enumerate(operations):
            machines, times = operation

            best_machine = -1
            min_end_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_num])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

            schedule[job_num].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = min_end_time
            job_completion_time[job_num] = min_end_time

    return schedule
