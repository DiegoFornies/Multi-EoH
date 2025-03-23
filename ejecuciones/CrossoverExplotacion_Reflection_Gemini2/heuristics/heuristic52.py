
def heuristic(input_data):
    """Schedules jobs to minimize makespan and balance load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id, operations in jobs.items():
        schedule[job_id] = []
        for op_idx, operation in enumerate(operations):
            machines, times = operation
            op_num = op_idx + 1
            
            best_machine, best_time = None, float('inf')
            earliest_start = float('inf')

            for i, machine in enumerate(machines):
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                completion_time = start_time + time

                # Prioritize machines that become available earlier
                if completion_time < earliest_start:
                    earliest_start = completion_time
                    best_machine = machine
                    best_time = time

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
            
    return schedule
