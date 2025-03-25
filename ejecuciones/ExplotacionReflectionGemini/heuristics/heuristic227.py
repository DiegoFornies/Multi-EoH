
def heuristic(input_data):
    """Combines SPT and machine load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    available_operations = []
    for job_id in jobs:
        available_operations.append((job_id, 1))

    while available_operations:
        best_op = None
        min_end_time = float('inf')

        for job_id, op_num in available_operations:
            machines, times = jobs[job_id][op_num - 1]
            
            earliest_start_time = float('inf')
            chosen_machine = None
            chosen_processing_time = None
            
            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], (schedule[job_id][-1]['End Time'] if job_id in schedule and job_id in schedule else 0)) if op_num > 1 else machine_available_times[m]
                end_time = start_time + times[m_idx]
                
                if end_time < min_end_time:
                    min_end_time = end_time
                    earliest_start_time = start_time
                    chosen_machine = m
                    chosen_processing_time = times[m_idx]
                elif end_time == min_end_time:
                    if machine_load[m] < machine_load[chosen_machine]:
                        earliest_start_time = start_time
                        chosen_machine = m
                        chosen_processing_time = times[m_idx]
                        

            if chosen_machine is not None: # check if a valid machine found
                best_op = (job_id, op_num, chosen_machine, chosen_processing_time, earliest_start_time)
        
        if best_op is None: # check if a valid operation found
            break # to prevent infinite looping
            
        job_id, op_num, assigned_machine, processing_time, start_time = best_op
        end_time = start_time + processing_time
        
        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({'Operation': op_num, 'Assigned Machine': assigned_machine, 'Start Time': start_time, 'End Time': end_time, 'Processing Time': processing_time})
        
        machine_available_times[assigned_machine] = end_time
        machine_load[assigned_machine] += processing_time

        available_operations.remove((job_id, op_num))

        if op_num < len(jobs[job_id]):
            available_operations.append((job_id, op_num + 1))
    
    return schedule
