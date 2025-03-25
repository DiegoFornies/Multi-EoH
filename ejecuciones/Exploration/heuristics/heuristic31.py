
def heuristic(input_data):
    """A heuristic for the FJSSP using a shortest processing time and earliest start time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize schedule, machine availability, and job completion times.
    schedule = {}
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Prioritize operations based on shortest processing time
    operation_queue = []
    for job_id, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            min_time = float('inf')
            best_machine = None
            for i in range(len(machines)):
                if times[i] < min_time:
                    min_time = times[i]
                    best_machine = machines[i]
            operation_queue.append((min_time, job_id, op_idx))  # (processing time, job_id, op_index)

    operation_queue.sort() #Sort by the process time to schedule the shortest operation.

    # Schedule operations
    for _, job_id, op_idx in operation_queue:
        machines, times = jobs[job_id][op_idx]
        best_machine = None
        min_end_time = float('inf')
        processing_time = None
        
        for i, machine in enumerate(machines):
            available_time = machine_availability[machine]
            start_time = max(available_time, job_completion_times[job_id])
            end_time = start_time + times[i]
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = times[i]

        start_time = max(machine_availability[best_machine], job_completion_times[job_id])
        end_time = start_time + processing_time
        machine_availability[best_machine] = end_time
        job_completion_times[job_id] = end_time

        if job_id not in schedule:
            schedule[job_id] = []
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
    
    return schedule
