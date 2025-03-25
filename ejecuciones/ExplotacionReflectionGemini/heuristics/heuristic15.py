
def heuristic(input_data):
    """A heuristic for FJSSP that considers machine load and operation duration."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for op_index, operation in enumerate(job_operations):
            machines, durations = operation
            best_machine, best_start_time, best_duration = None, float('inf'), None

            for machine_index, machine in enumerate(machines):
                duration = durations[machine_index]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_duration = duration

            machine_available_time[best_machine] = best_start_time + best_duration
            job_completion_time[job_id] = best_start_time + best_duration

            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_duration,
                'Processing Time': best_duration
            })

    return schedule
