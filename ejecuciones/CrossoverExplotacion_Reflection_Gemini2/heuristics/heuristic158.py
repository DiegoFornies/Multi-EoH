
def heuristic(input_data):
    """Hybrid heuristic: earliest finish time, SPT, machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id, operations in jobs.items():
        schedule[job_id] = []
        last_end_time = 0

        for op_idx, operation in enumerate(operations):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_weighted_finish = float('inf')
            min_processing_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available[machine], job_completion[job_id])
                finish_time = start_time + time

                idle_time = start_time - last_end_time if op_idx > 0 else 0
                weighted_finish = finish_time + 0.05 * machine_load[machine] - 0.02 * idle_time #Adjust weights
                
                if weighted_finish < min_weighted_finish:
                    min_weighted_finish = weighted_finish
                    best_machine = machine
                    best_time = time

                elif weighted_finish == min_weighted_finish and time < min_processing_time:
                    min_processing_time = time
                    best_machine = machine
                    best_time = time

            start_time = max(machine_available[best_machine], job_completion[job_id])
            end_time = start_time + best_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            machine_available[best_machine] = end_time
            job_completion[job_id] = end_time
            machine_load[best_machine] += best_time
            last_end_time = end_time

    return schedule
