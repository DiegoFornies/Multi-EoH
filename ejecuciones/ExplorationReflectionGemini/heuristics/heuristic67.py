
def heuristic(input_data):
    """Combines earliest availability and load balancing, sorted by machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_end_time = float('inf')

            machine_load = {}
            for machine in possible_machines:
                machine_load[machine] = machine_available_times[machine]

            sorted_machines = sorted(machine_load, key=machine_load.get)

            for machine in sorted_machines:
                machine_index = possible_machines.index(machine)
                processing_time = possible_times[machine_index]

                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                combined_metric = end_time

                if combined_metric < min_end_time:
                    min_end_time = combined_metric
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            machine_available_times[best_machine] = best_start_time + best_processing_time
            job_completion_times[job_id] = best_start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

    return schedule
