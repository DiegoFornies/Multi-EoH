
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes machines with less workload."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            # Find the machine with the earliest available time among feasible machines
            best_machine = None
            min_end_time = float('inf')
            processing_time = None
            
            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_load[machine], job_completion_times[job])
                end_time = start_time + time
                
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    processing_time = time

            # Schedule the operation on the best machine
            start_time = max(machine_load[best_machine], job_completion_times[job])
            end_time = start_time + processing_time
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine load and job completion time
            machine_load[best_machine] = end_time
            job_completion_times[job] = end_time

    return schedule
