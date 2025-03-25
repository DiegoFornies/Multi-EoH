
def heuristic(input_data):
    """
    Schedules jobs using a priority rule based on shortest processing time,
    minimizing makespan and balancing machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    eligible_operations = {}
    for job_id in jobs:
        eligible_operations[job_id] = 0  # Start with the first operation of each job

    scheduled_operations = 0
    total_operations = sum(len(ops) for ops in jobs.values())

    while scheduled_operations < total_operations:
        # Find the next operation to schedule based on priority
        best_job, best_machine, best_processing_time = None, None, float('inf')

        for job_id, op_index in eligible_operations.items():
            if op_index >= len(jobs[job_id]):
                continue # All operations already scheduled for this job

            machines, times = jobs[job_id][op_index]

            # Find the best machine for the current operation
            for i, machine in enumerate(machines):
                processing_time = times[i]
                if processing_time < best_processing_time:
                    best_processing_time = processing_time
                    best_machine = machine
                    best_job = job_id

        # Schedule the operation
        if best_job is not None:
            op_index = eligible_operations[best_job]
            machines, times = jobs[best_job][op_index]
            machine_index = machines.index(best_machine)
            processing_time = times[machine_index]

            start_time = max(machine_available_times[best_machine], job_completion_times[best_job])
            end_time = start_time + processing_time

            schedule[best_job].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine and job completion times
            machine_available_times[best_machine] = end_time
            job_completion_times[best_job] = end_time

            # Move to the next operation for the job
            eligible_operations[best_job] += 1
            scheduled_operations += 1
        else:
            #No operation can be scheduled, should not happen.
            break

    return schedule
