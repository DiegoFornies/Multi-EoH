
def heuristic(input_data):
    """
    Heuristic for FJSSP that considers shortest processing time and earliest machine availability.
    Prioritizes operations with shorter processing times and assigns them to the earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Flatten operations into a list for prioritization
    operations = []
    for job, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations by shortest processing time (SPT) of the first available machine
    operations.sort(key=lambda x: min(x[3]))  #x[3] is times

    for job, op_num, machines, times in operations:
        # Find the earliest available machine among feasible machines
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = times[i] # Corresponding processing time
        
        if job not in schedule:
            schedule[job] = []

        end_time = best_start_time + best_processing_time
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
