
def heuristic(input_data):
    """Schedules jobs using a shortest processing time first (SPT) heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {}

    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times, job))

    def calculate_priority(operation):
        """Calculates the priority of an operation based on shortest processing time."""
        job, op_idx, machines, times, _ = operation
        min_time = float('inf')
        for time in times:
            min_time = min(min_time, time)
        return min_time

    operations.sort(key=calculate_priority)

    scheduled_ops = set()

    for job, op_idx, machines, times, original_job in operations:
        if (job, op_idx) not in scheduled_ops:
            # Find machine with earliest available time among feasible machines
            best_machine = None
            earliest_start_time = float('inf')
            processing_time = None

            for i, machine in enumerate(machines):
                start_time = max(machine_time[machine], job_completion_time[original_job])  # Use original job
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    processing_time = times[i]

            # Schedule the operation
            start_time = earliest_start_time
            end_time = start_time + processing_time
            op_num = op_idx + 1

            if original_job not in schedule:  # Use original job
                schedule[original_job] = []

            schedule[original_job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_time[best_machine] = end_time
            job_completion_time[original_job] = end_time  # Use original job
            scheduled_ops.add((job, op_idx))

    return schedule
