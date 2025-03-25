
def heuristic(input_data):
    """
    Heuristic for FJSSP that minimizes makespan, idle time, and balances machine load
    by scheduling operations on the earliest available machine with shortest processing time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    operations = []
    for job_id, operations_list in jobs_data.items():
        for op_id, operation in enumerate(operations_list):
            operations.append((job_id, op_id + 1, operation))

    # Sort operations based on shortest processing time. Jobs' index is also a factor.
    operations.sort(key=lambda x: min(x[2][1]))

    for job_id, operation_id, operation_data in operations:
        machines, processing_times = operation_data
        best_machine = None
        min_end_time = float('inf')

        # Find the machine that results in the earliest completion time for this operation.
        for i, machine in enumerate(machines):
            available_time = machine_available_time[machine]
            start_time = max(available_time, job_completion_time[job_id])
            end_time = start_time + processing_times[i]

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_times[i]

        # Schedule the operation on the selected machine.
        schedule[job_id].append({
            'Operation': operation_id,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': min_end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times.
        machine_available_time[best_machine] = min_end_time
        job_completion_time[job_id] = min_end_time

    return schedule
