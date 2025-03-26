
def heuristic(input_data):
    """Schedules jobs minimizing makespan, considering machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    eligible_operations = []
    for job in range(1, n_jobs + 1):
        schedule[job] = []
        eligible_operations.append((job, 0)) # job and op_index

    scheduled_operations = 0
    while scheduled_operations < sum(len(ops) for ops in jobs.values()):
        # Find the most promising operation to schedule
        best_operation = None
        min_makespan_increase = float('inf')

        for job, op_index in eligible_operations:
            operation = jobs[job][op_index]
            machines, times = operation

            # Find the machine that minimizes makespan increase
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time

                # Calculate potential makespan increase
                potential_makespan_increase = max(0, end_time - max(machine_available_time.values()))

                # Consider machine load
                load_factor = machine_load[machine]

                # Combine makespan increase and load factor
                combined_metric = potential_makespan_increase + 0.05 * load_factor #Adjust

                if combined_metric < min_makespan_increase:
                    min_makespan_increase = combined_metric
                    best_operation = (job, op_index, machine, start_time, processing_time)
        
        # Schedule the best operation
        job, op_index, best_machine, best_start_time, best_processing_time = best_operation
        op_num = op_index + 1
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability, job completion time, and machine load
        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job] = best_start_time + best_processing_time
        machine_load[best_machine] += best_processing_time

        # Update eligible operations
        eligible_operations.remove((job, op_index))
        if op_index + 1 < len(jobs[job]):
            eligible_operations.append((job, op_index + 1))
        
        scheduled_operations += 1

    return schedule
