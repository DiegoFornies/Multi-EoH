
def heuristic(input_data):
    """Combines earliest finish time, machine load, and job idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id, operations in jobs.items():
        schedule[job_id] = []
        last_end_time = 0  # Track the end time of the previous operation in the job

        for op_idx, operation in enumerate(operations):
            machines, times = operation
            op_num = op_idx + 1
            
            best_machine, best_time, earliest_finish, best_start = None, float('inf'), float('inf'), float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                finish_time = start_time + time
                
                # Add a small penalty for machine load and idle time
                idle_time = start_time - last_end_time if op_idx > 0 else 0
                weighted_finish = finish_time + 0.1 * machine_load[machine] - 0.05 * idle_time

                if weighted_finish < earliest_finish:
                    earliest_finish = weighted_finish
                    best_machine = machine
                    best_time = time
                    best_start = start_time
            
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_time
            
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            machine_load[best_machine] += best_time
            last_end_time = end_time  # Update for the next operation
            
    return schedule
