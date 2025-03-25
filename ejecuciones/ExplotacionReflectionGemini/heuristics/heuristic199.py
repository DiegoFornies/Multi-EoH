
def heuristic(input_data):
    """Heuristic for FJSSP: SPT with load balancing and local search."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    # Phase 1: SPT with load balancing
    while available_operations:
        best_operation = None
        best_machine = None
        shortest_processing_time = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]
            
            eligible_machines = []
            for machine_idx, machine in enumerate(machines):
                eligible_machines.append((machine, times[machine_idx]))
                
            # Tie-breaking rule to use the machine with the earliest available time
            best_eligible_machine = None
            earliest_available_time = float('inf')
            for machine, time in eligible_machines:
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                if time < shortest_processing_time:
                    shortest_processing_time = time
                    best_operation = (job_id, op_idx)
                    best_eligible_machine = (machine, time)
                    earliest_available_time = start_time
                elif time == shortest_processing_time:
                    start_time = max(machine_available_time[machine], job_completion_time[job_id])
                    if start_time < earliest_available_time:
                        earliest_available_time = start_time
                        best_operation = (job_id, op_idx)
                        best_eligible_machine = (machine, time)
                
            if best_eligible_machine is not None:
                machine, processing_time = best_eligible_machine
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time
                schedule[job_id].append({
                    'Operation': op_idx + 1,
                    'Assigned Machine': machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })

                machine_available_time[machine] = end_time
                job_completion_time[job_id] = end_time
                available_operations.remove((job_id, op_idx))

                if op_idx + 1 < len(jobs[job_id]):
                    available_operations.append((job_id, op_idx + 1))

    # Phase 2: Local search for balance (operation swaps) - limited iterations
    def calculate_machine_load(sched):
        machine_load = {m: 0 for m in range(n_machines)}
        for job_id in sched:
            for operation in sched[job_id]:
                machine = operation['Assigned Machine']
                machine_load[machine] += operation['Processing Time']
        return machine_load

    def calculate_load_imbalance(machine_load):
        total_load = sum(machine_load.values())
        num_machines = len(machine_load)
        average_load = total_load / num_machines if num_machines > 0 else 0
        
        imbalance = sum([(load - average_load)**2 for load in machine_load.values()])
        return imbalance

    original_schedule = {job_id: list(ops) for job_id, ops in schedule.items()} 
    original_load = calculate_machine_load(original_schedule)
    original_imbalance = calculate_load_imbalance(original_load)

    num_iterations = min(n_jobs * n_machines, 100) # Limit iterations
    for _ in range(num_iterations):
        # Randomly select two jobs
        job1_id, job2_id = sorted( [int(j) for j in schedule.keys()][:2] )
        
        if len(schedule[job1_id]) == 0 or len(schedule[job2_id]) == 0:
            continue

        # Randomly select an operation from each job
        op1_idx = 0 #random.randint(0, len(schedule[job1_id]) - 1)
        op2_idx = 0 #random.randint(0, len(schedule[job2_id]) - 1)
        
        op1 = schedule[job1_id][op1_idx]
        op2 = schedule[job2_id][op2_idx]
        
        # Swap machines if possible
        machines1, times1 = jobs[job1_id][op1['Operation']-1]
        machines2, times2 = jobs[job2_id][op2['Operation']-1]

        if op2['Assigned Machine'] in machines1 and op1['Assigned Machine'] in machines2: #Feasibility check
            # Create a temporary schedule to test the swap
            temp_schedule = {job_id: list(ops) for job_id, ops in schedule.items()}

            #Find processing times for new Machines
            processing_time_op1 = times1[machines1.index(op2['Assigned Machine'])]
            processing_time_op2 = times2[machines2.index(op1['Assigned Machine'])]
            
            # Update the temporary schedule with the swapped machines and processing times
            temp_schedule[job1_id][op1_idx]['Assigned Machine'] = op2['Assigned Machine']
            temp_schedule[job1_id][op1_idx]['Processing Time'] = processing_time_op1
            temp_schedule[job2_id][op2_idx]['Assigned Machine'] = op1['Assigned Machine']
            temp_schedule[job2_id][op2_idx]['Processing Time'] = processing_time_op2

            temp_load = calculate_machine_load(temp_schedule)
            temp_imbalance = calculate_load_imbalance(temp_load)

            # Accept the swap if it improves load balance
            if temp_imbalance < original_imbalance:
                schedule[job1_id][op1_idx]['Assigned Machine'] = op2['Assigned Machine']
                schedule[job1_id][op1_idx]['Processing Time'] = processing_time_op1
                schedule[job2_id][op2_idx]['Assigned Machine'] = op1['Assigned Machine']
                schedule[job2_id][op2_idx]['Processing Time'] = processing_time_op2
                
                #Recalculate start/end times for changed jobs.
                #Reset all machine/job timings
                machine_available_time = {m: 0 for m in range(n_machines)}
                job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

                #Iterate Jobs, operations
                for job_id in range(1, n_jobs + 1):
                    for op_idx in range(len(schedule[job_id])):
                        machine = schedule[job_id][op_idx]['Assigned Machine']
                        processing_time = schedule[job_id][op_idx]['Processing Time']

                        start_time = max(machine_available_time[machine], job_completion_time[job_id])
                        end_time = start_time + processing_time
                
                        schedule[job_id][op_idx]['Start Time'] = start_time
                        schedule[job_id][op_idx]['End Time'] = end_time

                        machine_available_time[machine] = end_time
                        job_completion_time[job_id] = end_time

                original_imbalance = temp_imbalance

    return schedule
