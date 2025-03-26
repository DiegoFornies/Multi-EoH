
def heuristic(input_data):
    """Schedules jobs using a dynamic priority heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            # Dynamic priority: favor machines with smaller differences between their current load
            # and the average machine load.  This encourages load balancing.
            avg_load = sum(machine_time.values()) / n_machines if n_machines > 0 else 0
            best_machine = None
            min_diff = float('inf')

            for i in range(len(possible_machines)):
                machine = possible_machines[i]
                diff = abs(machine_time[machine] - avg_load)
                if diff < min_diff:
                    min_diff = diff
                    best_machine = machine
                    best_processing_time = possible_times[i]

            # Schedule operation to the best machine found
            start_time = max(machine_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job states
            machine_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return schedule
