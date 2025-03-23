
def heuristic(input_data):
    """Hybrid heuristic: Earliest finish, SPT, machine load, job sequencing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id, operations in jobs.items():
        schedule[job_id] = []
        for op_idx, operation in enumerate(operations):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_combined_score = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + time

                combined_score = 0.4 * end_time + 0.4 * machine_load[machine] + 0.2 * time

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_machine = machine
                    best_time = time
                    best_start_time = start_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_time,
                'Processing Time': best_time
            })

            machine_available_time[best_machine] = best_start_time + best_time
            job_completion_time[job_id] = best_start_time + best_time
            machine_load[best_machine] += best_time

    return schedule
