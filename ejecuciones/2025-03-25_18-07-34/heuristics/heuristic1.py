
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem that considers
    machine workload to balance the schedule. This heuristic aims to reduce
    makespan, separation, and balance the machine load by assigning operations to machines that are currently less busy.
    """
    schedule, machine_time = {}, {m: 0 for m in range(input_data['n_machines'])}
    
    for job, ops in input_data['jobs'].items():
        schedule[job], job_time = [], 0

        for op_idx, (machines, times) in enumerate(ops):
            op_num = op_idx + 1

            # Choose the machine with the earliest available time from the available machines
            best_machine, best_time, best_duration = None, float('inf'), float('inf')
            for m, t in zip(machines, times):
                available_time = max(machine_time[m], job_time)
                if available_time < best_time:
                    best_time = available_time
                    best_machine = m
                    best_duration = t
                elif available_time == best_time:
                    if t < best_duration:
                        best_machine = m
                        best_duration = t

            m = best_machine
            t = best_duration

            start = max(machine_time[m], job_time)
            end = start + t
            
            schedule[job].append({'Operation': op_num, 'Assigned Machine': m, 'Start Time': start, 'End Time': end, 'Processing Time': t})
            
            machine_time[m] = end
            job_time = end
    
    return schedule
