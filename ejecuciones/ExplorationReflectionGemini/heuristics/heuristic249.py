
def heuristic(input_data):
    """Adaptive SPT & load balancing for FJSSP. Chooses machine dynamically."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        ops = jobs[job_id]

        for op_idx, op_data in enumerate(ops):
            machines = op_data[0]
            times = op_data[1]

            best_machine, min_cost = None, float('inf')

            for i, machine in enumerate(machines):
                time = times[i]
                start = max(machine_available[machine], job_completion[job_id])
                end = start + time

                # Adaptive cost: SPT + dynamic load balancing
                load_factor = (machine_load[machine] / sum(machine_load.values())) if sum(machine_load.values())>0 else 0
                cost = time + 0.3 * load_factor * time + start * 0.01  # Adjusted weights

                if cost < min_cost:
                    min_cost = cost
                    best_machine, best_start, best_time = machine, start, time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start,
                'End Time': best_start + best_time,
                'Processing Time': best_time
            })

            machine_available[best_machine] = best_start + best_time
            job_completion[job_id] = best_start + best_time
            machine_load[best_machine] += best_time

    return schedule
