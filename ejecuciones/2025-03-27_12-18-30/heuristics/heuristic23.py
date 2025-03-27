
def heuristic(input_data):
    """Heuristic for FJSSP: Earliest Finish Time (EFT) with machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}  # Keep track of machine load

    for job in jobs:
        schedule[job] = []

    job_completion_time = {job: 0 for job in jobs}

    # Create a list of operations to schedule
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations based on the number of possible machines (SPT - shortest processing time)
    operations.sort(key=lambda x: len(x[2]))

    while operations:
        best_op = None
        best_machine = None
        earliest_finish_time = float('inf')

        for job, op_idx, machines, times in operations:
            # Find the earliest possible start time for this operation

            for machine_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job])
                finish_time = start_time + times[machine_idx]

                if finish_time < earliest_finish_time:
                    earliest_finish_time = finish_time
                    best_op = (job, op_idx, machines, times)
                    best_machine = machine
                    processing_time = times[machine_idx]

        # Schedule the best operation on the best machine
        job, op_idx, machines, times = best_op
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        machine_load[best_machine] += processing_time  # Update machine load
        job_completion_time[job] = end_time

        # Remove the scheduled operation from the list
        operations.remove(best_op)

    return schedule
