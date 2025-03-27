
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP)
    that considers machine idle time to minimize makespan, favoring
    machines that can execute operations sooner.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}

    for job_id, operations in jobs.items():
        schedule[job_id] = []
        for op_index, operation in enumerate(operations):
            machines = operation[0]
            processing_times = operation[1]

            best_machine = None
            best_start_time = float('inf')
            best_processing_time = None

            for machine_index, machine in enumerate(machines):
                processing_time = processing_times[machine_index]
                available_time = machine_available_times[machine]
                start_time = max(available_time, job_completion_times[job_id])

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = best_start_time
            end_time = start_time + best_processing_time
            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time

            schedule[job_id].append({
                'Operation': op_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

    return schedule
