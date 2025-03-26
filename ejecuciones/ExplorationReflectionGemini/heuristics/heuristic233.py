
def heuristic(input_data):
    """Prioritizes machines with the earliest expected completion time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_completion_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            # Find the machine with the earliest expected completion time.
            best_machine = None
            min_expected_completion = float('inf')
            best_processing_time = None

            for i, machine in enumerate(possible_machines):
                processing_time = possible_times[i]
                expected_completion = max(machine_completion_times[machine], job_completion_times[job_id]) + processing_time
                if expected_completion < min_expected_completion:
                    min_expected_completion = expected_completion
                    best_machine = machine
                    best_processing_time = processing_time

            # Schedule operation to the best machine found
            start_time = max(machine_completion_times[best_machine], job_completion_times[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job states
            machine_completion_times[best_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
