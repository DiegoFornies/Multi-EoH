
def heuristic(input_data):
    """Aims to minimize makespan by prioritizing operations with shortest processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Flatten operations into a list with job and operation indices
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations by shortest processing time first, then job number
    operations.sort(key=lambda x: min(x[3]))  # Sort by min processing time

    for job, op_num, machines, times in operations:
        best_machine, best_time = -1, float('inf')

        # Find the machine that results in the earliest completion time for the operation
        for i, machine in enumerate(machines):
            potential_start_time = max(machine_available_time[machine], job_completion_time[job])
            potential_end_time = potential_start_time + times[i]

            if potential_end_time < best_time:
                best_time = potential_end_time
                best_machine = machine
                processing_time = times[i]
                start_time = potential_start_time
        
        end_time = start_time + processing_time

        # Update schedule
        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
    return schedule
