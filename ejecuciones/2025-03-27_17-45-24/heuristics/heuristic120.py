
def heuristic(input_data):
    """
    FJSSP heuristic: Adapts between machine load balancing & EFT
    based on machine availability to minimize makespan and idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_loads = {m: 0 for m in range(n_machines)}

    schedule = {j: [] for j in range(1, n_jobs + 1)}

    remaining_operations = {}
    for job_id, operations in jobs_data.items():
        remaining_operations[job_id] = list(range(1, len(operations) + 1))

    scheduled_operations_count = 0
    total_operations = sum(len(ops) for ops in jobs_data.values())

    while scheduled_operations_count < total_operations:
        eligible_operations = []
        for job_id, operations in jobs_data.items():
            if remaining_operations[job_id]:
                op_index = remaining_operations[job_id][0] - 1
                eligible_operations.append((job_id, op_index))

        best_operation = None
        best_machine = None
        best_start_time = float('inf')
        
        # Adaptively choose between machine load and EFT.
        load_balance_priority = True # Start with load balance priority

        for job_id, op_index in eligible_operations:
            machines, times = jobs_data[job_id][op_index]

            # Calculate EFT for each machine.
            efts = []
            for m_index, machine in enumerate(machines):
                efts.append(max(machine_available_time[machine], job_completion_time[job_id]))

            # If load balance priority then prioritize less loaded machine
            if load_balance_priority:
                #Find the machine with the least load.
                available_machines = []
                for m_index, machine in enumerate(machines):
                    available_machines.append(machine_loads[machine])
                
                if len(available_machines) > 0:
                    machine_min_index = available_machines.index(min(available_machines)) # index of machine with min load
                    machine = machines[machine_min_index]
                    m_index = machine_min_index
                    start_time = max(machine_available_time[machine], job_completion_time[job_id])
                    processing_time = times[m_index] #Corresponding time to machine min

                    if start_time < best_start_time:
                        best_start_time = start_time
                        best_operation = (job_id, op_index)
                        best_machine = machine
                        best_processing_time = processing_time

            #If not priority use EFT rule.
            else:
                for m_index, machine in enumerate(machines):
                    start_time = max(machine_available_time[machine], job_completion_time[job_id])
                    if start_time < best_start_time:
                        best_start_time = start_time
                        best_operation = (job_id, op_index)
                        best_machine = machine
                        best_processing_time = times[m_index] #Corresponding time to the best_machine

        if best_operation is not None:
            job_id, op_index = best_operation
            start_time = best_start_time
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            machine_loads[best_machine] += best_processing_time

            remaining_operations[job_id].pop(0)
            scheduled_operations_count += 1

            # Potentially switch priority based on some criteria (e.g., machine availability).
            # Switch strategy
            if scheduled_operations_count % 5 == 0: # Check every 5 operations and switch
                load_balance_priority = not load_balance_priority

    return schedule
