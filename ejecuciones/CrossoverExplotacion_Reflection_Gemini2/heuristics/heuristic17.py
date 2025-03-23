
def heuristic(input_data):
    """
    Heuristic for FJSSP scheduling that prioritizes machines with the earliest available time.
    It assigns each operation to the machine with the minimum completion time
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs:
        schedule[job] = []
        operations = jobs[job]

        for op_idx, operation in enumerate(operations):
            op_num = op_idx + 1
            possible_machines = operation[0]
            processing_times = operation[1]

            best_machine = None
            min_completion_time = float('inf')

            for i, machine in enumerate(possible_machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])
                completion_time = start_time + processing_times[i]

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine
                    best_processing_time = processing_times[i]
                    best_start_time = start_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job] = best_start_time + best_processing_time

    return schedule
