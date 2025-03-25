
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations based on shortest processing time.
    It aims to balance machine load and minimize makespan by selecting machines
    and scheduling operations based on immediate availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a priority list of operations based on shortest processing time
    operation_queue = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            min_time = float('inf')
            best_machine = None
            for i in range(len(machines)):
                if times[i] < min_time:
                    min_time = times[i]
                    best_machine = machines[i]

            operation_queue.append((min_time, job_id, op_idx, machines, times))

    operation_queue.sort()  # Sort by shortest processing time

    for _, job_id, op_idx, machines, times in operation_queue:
        op_num = op_idx + 1

        # Find the earliest available machine among the feasible ones
        best_machine = None
        start_time = float('inf')
        processing_time = None

        for i, machine in enumerate(machines):
            available_time = max(machine_available_time[machine], job_completion_time[job_id])
            if available_time < start_time:
                start_time = available_time
                best_machine = machine
                processing_time = times[i]

        end_time = start_time + processing_time
        
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
