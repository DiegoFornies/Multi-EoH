
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations with shortest processing time 
    and earliest available machines, aiming to minimize makespan and machine idle time.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    scheduled_operations = {}

    # Create a list of operations, each containing job, operation number, and eligible machines
    operations = []
    for job_id, job_operations in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job_operations):
            operations.append({
                'job': job_id,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times
            })

    # Sort operations by shortest processing time
    operations.sort(key=lambda op: min(op['times']))

    while operations:
        best_op = None
        best_machine = None
        earliest_start = float('inf')

        for op in operations:
            for machine_idx, machine in enumerate(op['machines']):
                processing_time = op['times'][machine_idx]
                available_time = machine_available_time[machine]
                job_ready_time = job_completion_time[op['job']]
                start_time = max(available_time, job_ready_time)
                
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_op = op
                    best_machine = machine
                    best_processing_time = processing_time

        # Schedule the best operation on the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[best_op['job']])
        end_time = start_time + best_processing_time
        
        if best_op['job'] not in scheduled_operations:
            scheduled_operations[best_op['job']] = []

        scheduled_operations[best_op['job']].append({
            'Operation': best_op['operation'],
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[best_op['job']] = end_time

        operations.remove(best_op)

    return scheduled_operations
