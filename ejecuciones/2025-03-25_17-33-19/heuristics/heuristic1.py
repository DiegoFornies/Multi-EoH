
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes machines with the earliest available time
    and selects the operation with the shortest processing time among feasible machines.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_num in jobs:
        schedule[job_num] = []
        for op_idx, operation in enumerate(jobs[job_num]):
            machines, times = operation
            op_num = op_idx + 1

            # Find the machine with the earliest available time among feasible machines
            best_machine = None
            min_start_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_num])

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
            
            start_time = max(machine_available_time[best_machine], job_completion_time[job_num])
            end_time = start_time + best_processing_time
            
            schedule[job_num].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_num] = end_time
    
    return schedule
