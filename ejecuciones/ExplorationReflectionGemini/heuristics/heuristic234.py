
def heuristic(input_data):
    """Dynamic scheduling: Chooses machine based on workload and operation urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    remaining_ops = {j: len(jobs[j]) for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    completed_operations = {j: 0 for j in range(1, n_jobs + 1)}


    while any(remaining_ops[j] > 0 for j in range(1, n_jobs + 1)):
        eligible_operations = []
        for job_id in range(1, n_jobs + 1):
            if completed_operations[job_id] < len(jobs[job_id]):
                eligible_operations.append(job_id)

        for job_id in eligible_operations:
            operation_index = completed_operations[job_id]
            operation_data = jobs[job_id][operation_index]
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_end_time = float('inf')

            # Calculate machine urgency based on available time and jobs remaining
            machine_urgency = {}
            for machine in possible_machines:
                machine_urgency[machine] = machine_available_times[machine] # Lower = more urgent

            sorted_machines = sorted(machine_urgency, key=machine_urgency.get)

            for machine in sorted_machines:
                machine_index = possible_machines.index(machine)
                processing_time = possible_times[machine_index]

                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            machine_available_times[best_machine] = best_start_time + best_processing_time
            job_completion_times[job_id] = best_start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            completed_operations[job_id] += 1
            remaining_ops[job_id] -= 1

    return schedule
