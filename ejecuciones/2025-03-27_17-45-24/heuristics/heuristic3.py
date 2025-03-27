
def heuristic(input_data):
    """Schedules jobs using a least-loaded machine heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    
    for job in range(1, n_jobs + 1):
        schedule[job] = []
        job_end_time = 0
        
        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1
            
            # Find the machine with the earliest available time among feasible machines
            best_machine, best_time = None, float('inf')
            for m_idx, machine in enumerate(machines):
                available_time = max(machine_load[machine], job_end_time)
                if available_time < best_time:
                    best_time = available_time
                    best_machine = machine
                    processing_time = times[m_idx]  # Correct processing time
            
            if best_machine is None:
                raise ValueError("No feasible machine found for operation.")

            start_time = best_time
            end_time = start_time + processing_time
            
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            
            machine_load[best_machine] = end_time
            job_end_time = end_time
    
    return schedule
