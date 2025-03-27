
def heuristic(input_data):
    """Schedules operations on earliest available machine, considering operation order."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        operations = jobs[job_id]

        for op_idx, operation in enumerate(operations):
            machines, times = operation

            # Find the earliest available machine for this operation.
            earliest_start_time = float('inf')
            selected_machine = None
            selected_processing_time = None

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    selected_machine = machine
                    selected_processing_time = processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': selected_machine,
                'Start Time': earliest_start_time,
                'End Time': earliest_start_time + selected_processing_time,
                'Processing Time': selected_processing_time
            })

            machine_available_time[selected_machine] = earliest_start_time + selected_processing_time
            job_completion_time[job_id] = earliest_start_time + selected_processing_time

    return schedule
