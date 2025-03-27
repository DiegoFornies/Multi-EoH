
def heuristic(input_data):
    """FJSSP heuristic: Random assignment + local search."""
    import random

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initial random schedule
    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in jobs:
        schedule[job] = []
        current_time = 0
        for op_idx, op in enumerate(jobs[job]):
            machines, times = op
            # Randomly assign machine
            m_idx = random.randint(0, len(machines) - 1)
            machine = machines[m_idx]
            processing_time = times[m_idx]

            start_time = max(machine_time[machine], job_completion_time[job])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            machine_time[machine] = end_time
            job_completion_time[job] = end_time

    # Local search: Swap machine assignments for improvement.
    for _ in range(100):  # Iterate for some improvement rounds
        job1 = random.randint(1, n_jobs)
        op_idx1 = random.randint(0, len(jobs[job1]) - 1)
        
        #Find job 2 and operation 2
        job2 = random.randint(1, n_jobs)
        op_idx2 = random.randint(0, len(jobs[job2]) - 1)

        # Original makespan
        original_makespan = max(machine_time.values())
        
        #Backup current scheduling
        backup_schedule = {}
        backup_machine_time = machine_time.copy()
        backup_job_completion_time = job_completion_time.copy()
        
        backup_schedule = {job :[op.copy() for op in schedule[job]] for job in schedule}

        # Swap machine indices and recalculate the schedule
        machines1, times1 = jobs[job1][op_idx1]
        machines2, times2 = jobs[job2][op_idx2]
        
        original_machine1 = schedule[job1][op_idx1]['Assigned Machine']
        original_machine2 = schedule[job2][op_idx2]['Assigned Machine']
        
        #Find corresponding machine index
        m_idx1 = machines1.index(original_machine1)
        m_idx2 = machines2.index(original_machine2)

        
        machine1_index = machines1.index(original_machine1)
        machine2_index = machines2.index(original_machine2)
        
        #Choose another machine from machine list
        m_idx1_new = random.randint(0, len(machines1)-1)
        m_idx2_new = random.randint(0, len(machines2)-1)

        new_machine1 = machines1[m_idx1_new]
        new_machine2 = machines2[m_idx2_new]
        
        # Restore the initial conditions: time and completion
        machine_time = {m: 0 for m in range(n_machines)}
        job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
        schedule = {}
        for job in jobs:
            schedule[job] = []

        #Recalculate the schedule
        for job in jobs:
            current_time = 0
            for op_idx, op in enumerate(jobs[job]):
                machines, times = op
                
                if job == job1 and op_idx == op_idx1:
                    machine = new_machine1
                    processing_time = times[m_idx1_new]
                    
                elif job == job2 and op_idx == op_idx2:
                    machine = new_machine2
                    processing_time = times[m_idx2_new]
                else:
                    machine = schedule[job][op_idx]['Assigned Machine']
                    processing_time = schedule[job][op_idx]['Processing Time']
                
                start_time = max(machine_time[machine], job_completion_time[job])
                end_time = start_time + processing_time

                schedule[job].append({
                    'Operation': op_idx + 1,
                    'Assigned Machine': machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })
                machine_time[machine] = end_time
                job_completion_time[job] = end_time


        # New makespan
        new_makespan = max(machine_time.values())

        # Keep the change if it improves makespan
        if new_makespan < original_makespan:
            pass
        else:
            #Restore schedule
            schedule = backup_schedule
            machine_time = backup_machine_time
            job_completion_time = backup_job_completion_time
            # Restore original schedule
            
    return schedule
