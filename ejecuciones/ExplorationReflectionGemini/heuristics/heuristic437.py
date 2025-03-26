
def heuristic(input_data):
    """Operation-centric scheduling with lookahead for congestion."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    remaining_operations = {}
    for job_id in range(1, n_jobs + 1):
        remaining_operations[job_id] = 0

    def calculate_bottleneck_score(machine, start_time, processing_time):
        """Estimates machine congestion."""
        end_time = start_time + processing_time
        return max(0, end_time - machine_available_times[machine])

    def get_available_operations():
        """Finds operations ready to be scheduled."""
        available = []
        for job_id in range(1, n_jobs + 1):
            if remaining_operations[job_id] < len(jobs[job_id]):
                available.append((job_id, remaining_operations[job_id]))
        return available

    while True:
        available_operations = get_available_operations()
        if not available_operations:
            break

        best_operation = None
        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None
        min_bottleneck_score = float('inf')
        
        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                bottleneck_score = calculate_bottleneck_score(machine, start_time, processing_time)

                if bottleneck_score < min_bottleneck_score or (bottleneck_score == min_bottleneck_score and start_time < best_start_time):
                    min_bottleneck_score = bottleneck_score
                    best_operation = (job_id, op_idx)
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

        job_id, op_idx = best_operation
        
        machine_available_times[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        remaining_operations[job_id] += 1

    return schedule
