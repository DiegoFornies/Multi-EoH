
def heuristic(input_data):
    """
    A heuristic to schedule jobs on machines, prioritizing minimizing idle time and machine load balance.
    It selects the machine with the earliest available time for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}  # Completion time of each job

    for job_id, operations in jobs.items():
        schedule[job_id] = []
        for op_idx, op_data in enumerate(operations):
            machines, processing_times = op_data

            # Find the machine with the earliest available time among feasible machines
            best_machine = None
            min_available_time = float('inf')
            best_processing_time = None

            for i, machine in enumerate(machines):
                available_time = max(machine_available_times[machine], job_completion_times[job_id])
                if available_time < min_available_time:
                    min_available_time = available_time
                    best_machine = machine
                    best_processing_time = processing_times[i]

            # Schedule the operation on the chosen machine
            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job completion times
            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
