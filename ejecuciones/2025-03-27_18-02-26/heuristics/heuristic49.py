
def heuristic(input_data):
    """
    Prioritizes jobs with more operations. Minimizes idle time by
    scheduling operations as soon as possible on available machines.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Sort jobs by number of operations (descending)
    job_priority = sorted(jobs.keys(), key=lambda job_id: len(jobs[job_id]), reverse=True)

    for job_id in job_priority:
        schedule[job_id] = []
        operations = jobs[job_id]

        for op_index, operation in enumerate(operations):
            eligible_machines = operation[0]
            processing_times = operation[1]

            # Find the machine that allows for the earliest start time
            best_machine = None
            earliest_start = float('inf')
            best_processing_time = None

            for machine_index, machine_id in enumerate(eligible_machines):
                processing_time = processing_times[machine_index]
                start_time = max(machine_available_time[machine_id], job_completion_time[job_id])

                if start_time < earliest_start:
                    earliest_start = start_time
                    best_machine = machine_id
                    best_processing_time = processing_time

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
