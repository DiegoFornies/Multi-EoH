
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing machine idle time
    and balancing the workload across machines.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}  # Keep track of machine load
    
    for job in jobs:
        schedule[job] = []
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            # Find the machine with the earliest available time, considering job dependencies
            best_machine, best_time, best_start = None, float('inf'), None
            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])
                if start_time < best_time:
                    best_machine, best_time, best_start = machine, start_time, start_time
            
            processing_time = times[machines.index(best_machine)]

            # Schedule the operation on the selected machine
            start_time = best_start
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            
            # Update machine availability and job completion time
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time
            machine_load[best_machine] += processing_time
            
    return schedule
