
def heuristic(input_data):
    """Heuristic to solve the FJSSP, minimizing makespan and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}  # Initialize completion times for each job

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, (machines, times) in enumerate(jobs[job]):
            operation_number = op_idx + 1

            # Find the machine that allows the earliest operation completion, considering machine and job availability.
            best_machine = None
            earliest_end_time = float('inf')
            processing_time = None

            for machine_idx, machine in enumerate(machines):
                potential_start_time = max(machine_available_times[machine], job_completion_times[job])
                potential_end_time = potential_start_time + times[machine_idx]

                if potential_end_time < earliest_end_time:
                    earliest_end_time = potential_end_time
                    best_machine = machine
                    processing_time = times[machine_idx]

            # Schedule the operation on the selected machine
            start_time = max(machine_available_times[best_machine], job_completion_times[job])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine availability and job completion time
            machine_available_times[best_machine] = end_time
            job_completion_times[job] = end_time

    return schedule
