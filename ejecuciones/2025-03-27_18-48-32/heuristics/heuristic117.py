
def heuristic(input_data):
    """FJSSP heuristic: Random assignment with local search."""
    import random

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initial random schedule
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        current_time = 0
        for op_num in range(1, len(jobs_data[job]) + 1):
            machines, times = jobs_data[job][op_num - 1]
            chosen_machine = random.choice(machines)
            machine_idx = machines.index(chosen_machine)
            processing_time = times[machine_idx]
            start_time = max(machine_available_time[chosen_machine], job_completion_time[job])
            end_time = start_time + processing_time
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': chosen_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            machine_available_time[chosen_machine] = end_time
            job_completion_time[job] = end_time

    # Local search: Swap machine assignments for improvement
    def calculate_makespan(schedule):
        makespan = 0
        for job_schedule in schedule.values():
            for operation in job_schedule:
                makespan = max(makespan, operation['End Time'])
        return makespan
    
    best_makespan = calculate_makespan(schedule)
    
    for _ in range(100): # Number of iterations
        job1 = random.randint(1, n_jobs)
        job2 = random.randint(1, n_jobs)
        if job1 == job2:
          continue
        op_num1 = random.randint(0, len(jobs_data[job1]) -1 ) + 1
        op_num2 = random.randint(0, len(jobs_data[job2]) -1 ) + 1
        
        #Create a copy of schedule for modifications
        temp_schedule = {job: list(operations) for job, operations in schedule.items()}
        
        # Find corresponding machine indices and old machines for both operations
        machine_idx1 = temp_schedule[job1][op_num1-1]['Assigned Machine']
        machine_idx2 = temp_schedule[job2][op_num2-1]['Assigned Machine']
        
        # Store temporary operations
        temp_op1 = temp_schedule[job1][op_num1-1].copy()
        temp_op2 = temp_schedule[job2][op_num2-1].copy()

        machines1, times1 = jobs_data[job1][op_num1-1]
        machines2, times2 = jobs_data[job2][op_num2-1]
        
        #Check if swap is possible by checking if old machine is in operation
        if machine_idx2 in machines1 and machine_idx1 in machines2:
            # Find corresponding index from the machine list
            processing_time1 = times1[machines1.index(machine_idx2)]
            processing_time2 = times2[machines2.index(machine_idx1)]
        
            #Update the copies operation with changed Assigned Machine
            temp_op1['Assigned Machine'] = machine_idx2
            temp_op1['Processing Time'] = processing_time1
            
            temp_op2['Assigned Machine'] = machine_idx1
            temp_op2['Processing Time'] = processing_time2
            
            # Update the temporary schedule
            temp_schedule[job1][op_num1-1] = temp_op1
            temp_schedule[job2][op_num2-1] = temp_op2
            
            #Update the Time
            machine_available_time_temp = {m: 0 for m in range(n_machines)}
            job_completion_time_temp = {j: 0 for j in range(1, n_jobs + 1)}
            
            for job_id in range(1,n_jobs+1):
                current_time = 0
                for idx in range(len(temp_schedule[job_id])):
                    machine_id = temp_schedule[job_id][idx]['Assigned Machine']
                    processing_time = temp_schedule[job_id][idx]['Processing Time']
                    start_time = max(machine_available_time_temp[machine_id], job_completion_time_temp[job_id])
                    end_time = start_time+ processing_time
                    
                    temp_schedule[job_id][idx]['Start Time'] = start_time
                    temp_schedule[job_id][idx]['End Time'] = end_time
                    
                    machine_available_time_temp[machine_id] = end_time
                    job_completion_time_temp[job_id] = end_time
                    
            #Calculate new makespan
            new_makespan = calculate_makespan(temp_schedule)
                
            if new_makespan < best_makespan:
                best_makespan = new_makespan
                schedule = {job: list(operations) for job, operations in temp_schedule.items()}
                machine_available_time = {m: 0 for m in range(n_machines)}
                job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
                for job_id in range(1,n_jobs+1):
                    current_time = 0
                    for idx in range(len(schedule[job_id])):
                        machine_id = schedule[job_id][idx]['Assigned Machine']
                        end_time = schedule[job_id][idx]['End Time']
                        machine_available_time[machine_id] = end_time
                        job_completion_time[job_id] = end_time
    
    return schedule
