
def heuristic(input_data):
    """FJSSP heuristic: Combines SPT, load balancing, and dynamic machine selection."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_cost = float('inf')

            # Prioritize machines with lower load
            machine_load_subset = {}
            for machine in possible_machines:
                machine_load_subset[machine] = machine_available_times[machine]

            sorted_machines = sorted(machine_load_subset, key=machine_load_subset.get) # sort by load

            for machine in sorted_machines:
                machine_index = possible_machines.index(machine)
                processing_time = possible_times[machine_index]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                # Cost function: SPT + load balancing + sequence priority
                cost = processing_time + 0.1 * machine_load[machine] + start_time * 0.001

                if cost < min_cost:
                    min_cost = cost
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_times[best_machine] = best_start_time + best_processing_time
            job_completion_times[job_id] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time

    return schedule
