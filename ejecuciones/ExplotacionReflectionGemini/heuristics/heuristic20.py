
def heuristic(input_data):
    """A heuristic for FJSSP that considers machine load and operation dependencies."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Prioritize jobs with earlier due dates or fewer remaining operations.
    job_priority = {}
    for job_id in range(1, n_jobs + 1):
        job_priority[job_id] = (len(jobs_data[job_id])) # Number of operations
    
    sorted_jobs = sorted(job_priority.items(), key=lambda item: item[1]) # Sort jobs

    for job_id, _ in sorted_jobs:
        schedule[job_id] = []
        job_operations = jobs_data[job_id]

        for op_idx, operation in enumerate(job_operations):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_end_time = float('inf')

            # Evaluate each possible machine for the current operation.
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                end_time = start_time + processing_time

                # Choose the machine that results in the earliest completion of the operation, also consider balancing of machines.
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            # Schedule the operation on the chosen machine.
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability and job completion time.
            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_last_end_time[job_id] = best_start_time + best_processing_time

    return schedule
