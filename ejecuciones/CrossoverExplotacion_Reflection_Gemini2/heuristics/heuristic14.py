
def heuristic(input_data):
    """A heuristic to schedule jobs minimizing makespan by prioritizing jobs with more operations and machines with less workload.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}

    # Prioritize jobs with more operations.
    job_priority = sorted(jobs.keys(), key=lambda job: len(jobs[job]), reverse=True)

    for job in job_priority:
        schedule[job] = []
        current_time = 0

        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            # Find the machine with the earliest available time among feasible machines.
            best_machine = None
            min_end_time = float('inf')
            best_time = None
            
            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                
                start_time = max(machine_available_time[machine], job_completion_time[job]) #Respects job dependencies
                end_time = start_time + processing_time
                
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_time = processing_time
            
            if best_machine is None:
                print("No feasible machine found for operation", op_num, "of job", job)
                return None
            
            start_time = max(machine_available_time[best_machine], job_completion_time[job])
            end_time = start_time + best_time
            
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })
            
            machine_available_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
