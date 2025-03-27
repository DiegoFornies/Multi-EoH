
def heuristic(input_data):
    """A heuristic for FJSSP scheduling that considers machine load and job completion time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Step 1: Sort operations by shortest processing time (SPT) considering available machines
    operations = []
    for job_id, job_ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, machines, times))

    operations.sort(key=lambda op: min(op[3])) # Sort operations by minimum processing time across machines

    # Step 2: Assign operations to machines based on earliest completion time (ECT) heuristic
    for job_id, op_num, machines, times in operations:
        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            processing_time = times[m_idx]
            completion_time = start_time + processing_time

            if completion_time < best_start_time:
                best_machine, best_start_time, best_processing_time = machine, start_time, processing_time

        # Assign the operation to the best machine
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability and job completion time
        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job_id] = best_start_time + best_processing_time

    return schedule
