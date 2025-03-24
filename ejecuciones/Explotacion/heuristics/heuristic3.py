
def heuristic(input_data):
    """
    Heuristic for FJSSP that prioritizes minimizing machine idle time and operation start times.
    It considers available machines and processing times for each operation, assigning the machine
    that allows the earliest operation completion, thus balancing machine load.
    """
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}
    schedule = {}

    for job_id, operations in jobs.items():
        schedule[job_id] = []
        for op_idx, operation in enumerate(operations):
            machines, times = operation
            op_num = op_idx + 1

            # Find the machine that allows the earliest completion time for this operation
            best_machine = None
            min_completion_time = float('inf')
            best_processing_time = None

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                completion_time = start_time + processing_time

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Assign the operation to the best machine
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine available time and job completion time
            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
