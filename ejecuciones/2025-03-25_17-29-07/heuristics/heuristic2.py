
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) that considers machine load
    and operation durations to minimize makespan and balance machine utilization.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job = jobs[job_id]

        for op_idx, operation in enumerate(job):
            machines, durations = operation
            op_num = op_idx + 1

            # Select the machine with the earliest available time that can perform the operation.
            best_machine = None
            min_end_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                duration = durations[i]

                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + duration

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_duration = duration

            # Schedule the operation on the selected machine.
            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + best_duration

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_duration
            })

            # Update machine availability and job completion time.
            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
