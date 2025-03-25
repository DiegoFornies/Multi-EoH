
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes operations with the shortest processing time
    and assigns them to the machine with the earliest available time, minimizing makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of all operations with their job and operation number
    operations = []
    for job_id, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append((job_id, op_idx + 1, machines, times))

    # Sort operations by shortest processing time (SPT)
    operations.sort(key=lambda x: min(x[3]))  # x[3] are processing times

    for job_id, op_num, machines, times in operations:
        best_machine = None
        min_end_time = float('inf')

        # Find the machine that can process the operation earliest
        for i in range(len(machines)):
            machine = machines[i]
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time
        
        if job_id not in schedule:
            schedule[job_id] = []

        # Schedule the operation on the selected machine
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job_id] = best_start_time + best_processing_time

    return schedule
