
def heuristic(input_data):
    """FJSSP heuristic: adaptive strategy balancing makespan, separation."""
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

    # Adaptive weight for makespan vs. separation
    makespan_weight = 0.5
    separation_weight = 0.5

    while scheduled_operations_count < total_operations:
        eligible_operations = []
        for job_id, operations in jobs_data.items():
            if remaining_operations[job_id]:
                op_index = remaining_operations[job_id][0] - 1
                eligible_operations.append((job_id, op_index))

        best_operation = None
        best_machine = None
        best_score = float('inf')

        for job_id, op_index in eligible_operations:
            machines, times = jobs_data[job_id][op_index]

            for m_index, machine in enumerate(machines):
                processing_time = times[m_index]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                # Makespan component: prioritize earlier start times
                makespan_score = start_time

                # Separation component: prioritize machines with lower load
                separation_score = machine_loads[machine]

                # Weighted score
                score = makespan_weight * makespan_score + separation_weight * separation_score

                if score < best_score:
                    best_score = score
                    best_operation = (job_id, op_index)
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time
                    best_end_time = end_time

        if best_operation is not None:
            job_id, op_index = best_operation
            start_time = best_start_time
            end_time = best_end_time
            processing_time = best_processing_time
            machine = best_machine
            

            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[machine] = end_time
            job_completion_time[job_id] = end_time
            machine_loads[machine] += processing_time

            remaining_operations[job_id].pop(0)
            scheduled_operations_count += 1

            #Adaptive adjustment of weights (Optional and Experimental)
            #Consider historical data or real time performance
            #Here is an example, adjust weights slightly based on machine load:
            avg_machine_load = sum(machine_loads.values())/ len(machine_loads)
            if machine_loads[machine] > avg_machine_load:
                 separation_weight += 0.01 #Slightly increase Separation
                 makespan_weight -= 0.01 #Slightly Decrease makespan
            else:
                 separation_weight -= 0.005  #Slightly decrease Separation
                 makespan_weight += 0.005 #Slightly Increase makespan
            separation_weight = max(0.1, min(0.9, separation_weight))
            makespan_weight = max(0.1, min(0.9, makespan_weight))
        else:
            #Handle the situation where no operation can be scheduled.
            #This prevents an infinite loop in some scenarios.
            #For demonstration purpose, break the loop
            break

    return schedule
