
def heuristic(input_data):
    """A heuristic for the FJSSP that prioritizes minimizing idle time on machines."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}  # Tracks when each machine is next available
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}   # Tracks when each job is last completed
    machine_job_queue = {m: [] for m in range(n_machines)}       # Queues of jobs waiting for each machine

    # Initialize schedule structure
    for job in jobs:
        schedule[job] = []

    # Create a list of operations, sorted by job and operation number
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, op_data))

    # Iterate through operations, assigning them to machines based on a heuristic
    while operations:
        best_op = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, op_num, op_data in operations:
            machines, times = op_data

            # Consider only feasible machines for the operation
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]

                # Calculate earliest possible start time for this machine
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                # Prioritize machines to minimize finish time, then minimize queue length
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_op = (job_id, op_num, op_data)
                    best_machine = machine

        # If no operation found (shouldn't happen unless input is invalid), break
        if best_op is None:
            break

        job_id, op_num, op_data = best_op
        machines, times = op_data
        m_idx = machines.index(best_machine)
        processing_time = times[m_idx]

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        # Add operation to schedule
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        # Remove assigned operation from the list
        operations.remove(best_op)

    return schedule
