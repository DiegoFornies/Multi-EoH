
def heuristic(input_data):
    """Schedules jobs greedily, balancing makespan, idle time, and separation."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    # Initialize schedule
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    # Create a priority queue for available operations
    import heapq
    available_operations = []
    for job_id in range(1, n_jobs + 1):
        heapq.heappush(available_operations, (0, job_id, 0))  # (priority, job_id, operation_index)

    scheduled_operations = set()

    while available_operations:
        _, job_id, op_idx = heapq.heappop(available_operations)

        machines, times = jobs[job_id][op_idx]

        best_machine = None
        earliest_start_time = float('inf')

        for machine_idx, machine in enumerate(machines):
            processing_time = times[machine_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            
            # Heuristic score: prioritize machines with low load and earliest start time
            score = start_time + machine_load[machine]
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = (machine, processing_time)
                best_score = score
            elif start_time == earliest_start_time and machine_load[machine] < machine_load[best_machine[0]]:
                best_machine = (machine, processing_time)
                best_score = score
                
        machine, processing_time = best_machine

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
        machine_load[machine] += processing_time # update the machine's load

        # Add the next operation of the job if it exists
        if op_idx + 1 < len(jobs[job_id]):
            heapq.heappush(available_operations, (job_completion_time[job_id], job_id, op_idx + 1))

    return schedule
