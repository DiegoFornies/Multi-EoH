
def heuristic(input_data):
    """FJSSP heuristic: Combines SPT, dynamic load balancing, and job criticality."""
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
            best_start_time = 0
            best_processing_time = 0

            remaining_ops = len(job_operations) - operation_index
            job_criticality = remaining_ops # Higher criticality for jobs w/ more remaining ops

            for i, machine in enumerate(possible_machines):
                processing_time = possible_times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time
                
                # Adaptive weight based on machine load relative to average.
                avg_load = sum(machine_load.values()) / n_machines if n_machines else 0 # Handling zero division
                load_weight = 0.1 if machine_load[machine] <= avg_load else 0.5
                
                # Cost: SPT + load balance + job criticality + job waiting time
                cost = processing_time + load_weight * machine_load[machine] - 0.05 * job_criticality + 0.01 * start_time

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
