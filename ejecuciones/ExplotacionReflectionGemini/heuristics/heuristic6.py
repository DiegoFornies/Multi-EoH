
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes shorter processing times and earlier machine availability."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    
    for job in jobs:
        schedule[job] = []

    # Create a list of operations sorted by shortest processing time first, then job number.
    eligible_operations = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            eligible_operations.append((times[0], job_id, op_idx, machines, times))
            
    eligible_operations.sort()  # Sort by processing time then job id

    while eligible_operations:
        _, job_id, op_idx, machines, times = eligible_operations.pop(0)
        operation_number = op_idx + 1

        # Find the best machine for the operation
        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time
        
        end_time = best_start_time + best_processing_time

        schedule[job_id].append({
            'Operation': operation_number,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
