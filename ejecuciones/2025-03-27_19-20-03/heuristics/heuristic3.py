
def heuristic(input_data):
    """
    Schedules jobs heuristically, prioritizing shortest processing time and earliest machine availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}  # Stores the final schedule
    machine_available_time = {m: 0 for m in range(n_machines)}  # Tracks when each machine is next available
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}  # Tracks when each job's previous operation is completed

    # List of all operations, sorted by shortest processing time
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations using SPT rule modified to find best machine.
    operations.sort(key=lambda x: min(x[3]))

    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1

        # Find the machine that can start the operation earliest
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < best_start_time:
                best_machine = machine
                best_start_time = start_time
                best_processing_time = times[m_idx] # Get correct processing time for that machine

        # Schedule the operation on the best machine
        end_time = best_start_time + best_processing_time

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

        # Add scheduled operation to the schedule
        if job not in schedule:
            schedule[job] = []
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
    
    return schedule
