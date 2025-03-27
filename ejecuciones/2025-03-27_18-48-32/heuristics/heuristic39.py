
def heuristic(input_data):
    """Heuristic for FJSSP: Prioritizes critical path and balanced machine load."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Calculate total work (processing time) for each job
    job_work = {}
    for job_id, operations in jobs.items():
        total_work = sum(min(op[1]) for op in operations) # Use shortest processing time for calculation
        job_work[job_id] = total_work

    # Sort jobs by their total work in descending order (longest jobs first)
    sorted_jobs = sorted(job_work.items(), key=lambda item: item[1], reverse=True)

    for job_id, _ in sorted_jobs:
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]

            # Find machine with earliest completion time, considering load balancing
            best_machine = None
            min_end_time = float('inf')

            for i, machine_id in enumerate(possible_machines):
                processing_time = possible_times[i]
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, current_time)
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine_id

            # Schedule operation on the best machine
            processing_time = possible_times[possible_machines.index(best_machine)]
            start_time = max(machine_available_times[best_machine], current_time)
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_times[best_machine] = end_time
            current_time = end_time
            job_completion_times[job_id] = end_time # Update job completion time

    return schedule
