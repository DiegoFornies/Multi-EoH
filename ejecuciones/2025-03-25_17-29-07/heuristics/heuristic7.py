
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem that prioritizes
    minimizing idle time on machines and balancing workload across machines.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Initialize job completion times

    # Create a list of operations with job, op_idx and operation details
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations based on shortest processing time.
    operations.sort(key=lambda op: min(op[3])) #Sort based on shortest processing time amongst possible times

    for job, op_num, machines, times in operations:
        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        # Find the machine that minimizes idle time + job waiting time
        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            
            if start_time < best_start_time:
                best_machine, best_start_time, best_processing_time = machine, start_time, processing_time

        # If no suitable machine found, use first available
        if best_machine is None:
            best_machine = machines[0]
            best_processing_time = times[0]
            best_start_time = max(machine_available_time[best_machine], job_completion_time[job])
            
        end_time = best_start_time + best_processing_time
        
        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
    return schedule
