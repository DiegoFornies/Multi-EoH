
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes minimizing idle time
    and balancing machine load.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    machine_assignments = {m: [] for m in range(n_machines)}

    # Initialize schedule for each job
    for job_id in jobs:
        schedule[job_id] = []

    # Schedule operations
    for job_id in jobs:
        for op_idx, op_data in enumerate(jobs[job_id]):
            eligible_machines = op_data[0]
            processing_times = op_data[1]
            op_num = op_idx + 1

            best_machine = -1
            min_completion_time = float('inf')

            # Find the best machine for the current operation
            for i, machine_id in enumerate(eligible_machines):
                processing_time = processing_times[i]
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                completion_time = start_time + processing_time

                # Choose the machine that minimizes the completion time, prioritize machine load
                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine_id
            
            # Assign to the best machine
            assigned_machine = best_machine
            processing_time = processing_times[eligible_machines.index(assigned_machine)]

            available_time = machine_available_times[assigned_machine]
            start_time = max(available_time, job_completion_times[job_id])
            end_time = start_time + processing_time

            # Update machine and job times
            machine_available_times[assigned_machine] = end_time
            job_completion_times[job_id] = end_time
            machine_assignments[assigned_machine].append((job_id, op_num, start_time, end_time))

            # Append this operation to job schedule
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': assigned_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
    return schedule
