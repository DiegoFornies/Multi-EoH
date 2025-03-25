
def heuristic(input_data):
    """
    Schedules jobs based on shortest processing time and earliest available machine.
    Prioritizes jobs with fewer remaining operations.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    remaining_operations = {j: len(jobs_data[j]) for j in range(1, n_jobs + 1)}

    unscheduled_operations = []
    for job_id, operations in jobs_data.items():
        for op_idx, op_data in enumerate(operations):
            unscheduled_operations.append((job_id, op_idx, op_data))

    # Sort operations by job with fewer remaining operations first
    unscheduled_operations.sort(key=lambda x: remaining_operations[x[0]])

    while unscheduled_operations:
        best_operation = None
        best_machine = None
        earliest_start = float('inf')

        for job_id, op_idx, op_data in unscheduled_operations:
            machines, times = op_data

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < earliest_start:
                    earliest_start = start_time
                    best_operation = (job_id, op_idx, op_data)
                    best_machine = machine
                    best_processing_time = processing_time

        job_id, op_idx, op_data = best_operation
        op_num = op_idx + 1

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        remaining_operations[job_id] -= 1

        unscheduled_operations.remove(best_operation)
        # Re-sort after scheduling an operation
        unscheduled_operations.sort(key=lambda x: remaining_operations[x[0]])
            
    return schedule
