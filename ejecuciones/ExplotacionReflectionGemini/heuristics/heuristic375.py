
def heuristic(input_data):
    """Combines greedy makespan and machine availability to schedule jobs."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    eligible_operations = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            eligible_operations.append((job_id, op_idx, machines, times))
    
    scheduled_operations = set()

    while len(scheduled_operations) < sum(len(ops) for ops in jobs.values()):
        best_operation = None
        best_machine = None
        earliest_end_time = float('inf')

        for job_id, op_idx, machines, times in eligible_operations:
            if (job_id, op_idx) in scheduled_operations:
                continue
            
            preceding_operations_scheduled = True
            for prev_op_idx in range(op_idx):
                if (job_id, prev_op_idx) not in scheduled_operations:
                    preceding_operations_scheduled = False
                    break
                    
            if not preceding_operations_scheduled:
                continue
            
            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < earliest_end_time:
                    earliest_end_time = end_time
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)

        if best_operation:
            job_id, op_idx = best_operation
            machines, times = jobs[job_id][op_idx]
            machine_idx = machines.index(best_machine[0]) #Find correct machine_idx
            processing_time = best_machine[1]
            machine = best_machine[0]

            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            machine_available_time[machine] = end_time
            job_completion_time[job_id] = end_time
            scheduled_operations.add((job_id, op_idx))

    return schedule
