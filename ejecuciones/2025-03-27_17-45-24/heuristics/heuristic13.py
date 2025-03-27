
def heuristic(input_data):
    """Schedules jobs on machines, prioritizing machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)} # keep track of current machine load

    for job in jobs:
        schedule[job] = []
        job_completion_time = 0  # Completion time of the previous operation of current job

        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1
            # Find the machine with the earliest available time considering also machine load.
            best_machine = None
            min_end_time = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                available_time = max(machine_available_time[machine], job_completion_time)
                end_time = available_time + processing_time

                # Adjust the end time consideration based on machine load
                load_factor = 1 + machine_load[machine] / sum(machine_load.values()) if sum(machine_load.values()) > 0 else 1
                adjusted_end_time = end_time * load_factor  # higher load implies a higher adjusted end time
                
                if adjusted_end_time < min_end_time:
                    min_end_time = adjusted_end_time
                    best_machine = machine
                    best_start_time = available_time
                    best_processing_time = processing_time
            
            # Schedule the operation on the best machine
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })
            
            # Update machine available time, machine load, and job completion time
            machine_available_time[best_machine] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_time = best_start_time + best_processing_time
    
    return schedule
