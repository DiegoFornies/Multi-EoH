
def heuristic(input_data):
    """Schedules jobs using a machine load balancing heuristic.

    Prioritizes operations on machines with the earliest available time,
    balancing machine load and minimizing makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {}

    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations by job number and operation index
    operations.sort(key=lambda x: (x[0], x[1]))

    scheduled_ops = set()

    while len(scheduled_ops) < len(operations):
        # Find eligible operations (not yet scheduled and respecting job sequence)
        eligible_operations = []
        for job, op_idx, machines, times in operations:
            if (job, op_idx) not in scheduled_ops:
                # Check job sequence feasibility
                if op_idx == 0 or ((job, op_idx - 1) in scheduled_ops and
                                    job_completion_time[job] > 0):  # Ensure previous operation is completed
                    eligible_operations.append((job, op_idx, machines, times))

        # If no eligible operations, break to avoid infinite loop
        if not eligible_operations:
            break

        # Select the best operation based on machine availability
        best_op = None
        best_machine = None
        earliest_start_time = float('inf')

        for job, op_idx, machines, times in eligible_operations:
            #Find the machine with earliest available time
            available_machines = []
            for idx, machine in enumerate(machines):
                available_machines.append((machine, times[idx]))
            
            best_available_time = float('inf')
            best_available_machine = None

            for m, t in available_machines:
                start_time = max(machine_time[m], job_completion_time[job])
                if start_time < best_available_time:
                    best_available_time = start_time
                    best_available_machine = m

            if best_available_time < earliest_start_time:
                earliest_start_time = best_available_time
                best_op = (job, op_idx, machines, times)
                best_machine = best_available_machine

        # Schedule the best operation
        if best_op is not None:
            job, op_idx, machines, times = best_op
            op_num = op_idx + 1

            processing_time = times[machines.index(best_machine)]

            start_time = max(machine_time[best_machine], job_completion_time[job])
            end_time = start_time + processing_time

            if job not in schedule:
                schedule[job] = []

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_time[best_machine] = end_time
            machine_load[best_machine] += processing_time
            job_completion_time[job] = end_time
            scheduled_ops.add((job, op_idx))

    return schedule
