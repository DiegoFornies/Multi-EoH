
def heuristic(input_data):
    """A simple heuristic that schedules operations greedily."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_num in range(1, n_jobs + 1):
        schedule[job_num] = []
        operations = jobs[job_num]

        for op_idx, operation in enumerate(operations):
            machines, times = operation

            # Find the best machine for the current operation
            best_machine = -1
            min_completion_time = float('inf')
            best_processing_time = 0

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_num])
                completion_time = start_time + processing_time

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            # Schedule the operation on the chosen machine
            schedule[job_num].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_completion_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability and job completion time
            machine_available_time[best_machine] = min_completion_time
            job_completion_time[job_num] = min_completion_time

    return schedule
