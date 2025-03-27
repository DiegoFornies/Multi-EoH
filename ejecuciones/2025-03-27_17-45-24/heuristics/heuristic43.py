
def heuristic(input_data):
    """Schedules jobs minimizing makespan using a Shortest Processing Time (SPT) rule with tie-breaking for balanced workload."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        job_completion_time = 0

        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1
            
            # SPT rule: Choose the machine with shortest processing time
            best_machine = None
            min_processing_time = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                if processing_time < min_processing_time:
                    min_processing_time = processing_time
                    best_machine = machine

            # Schedule the operation on the selected machine.
            processing_time = times[machines.index(best_machine)]
            start_time = max(machine_available_time[best_machine], job_completion_time)
            end_time = start_time + processing_time
            
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            
            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += processing_time
            job_completion_time = end_time
    
    return schedule
