
def heuristic(input_data):
    """FJSSP heuristic: SPT & load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    for job in jobs:
        op_num = 1
        current_time = 0

        for machines, times in jobs[job]:
            best_machine = None
            min_end_time = float('inf')
            best_processing_time = None

            for i, machine in enumerate(machines):
                start_time = max(current_time, machine_load[machine])
                end_time = start_time + times[i]
                cost = end_time + 0.1 * machine_load[machine]  # Load balancing factor

                if cost < min_end_time:
                    min_end_time = cost
                    best_machine = machine
                    best_processing_time = times[i]
                    best_start_time = start_time
                    best_end_time = end_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_end_time,
                'Processing Time': best_processing_time
            })

            machine_load[best_machine] = best_end_time
            current_time = best_end_time
            job_completion_times[job] = best_end_time
            op_num += 1
    return schedule
