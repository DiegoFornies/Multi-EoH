
def heuristic(input_data):
    """FJSSP Heuristic: Combines SPT, load balancing, and job urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    job_remaining_times = {}
    machine_load = {m: 0 for m in range(n_machines)}


    for job_id in range(1, n_jobs + 1):
        remaining_time = 0
        for machines, times in jobs[job_id]:
            remaining_time += min(times)
        job_remaining_times[job_id] = remaining_time


    for job_id in range(1, n_jobs + 1):
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            best_machine = None
            min_cost = float('inf')

            for i, machine in enumerate(possible_machines):
                processing_time = possible_times[i]

                start_time = max(machine_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time
                # Cost combining SPT, machine load, and job urgency.

                cost = processing_time + 0.2 * machine_load[machine] + start_time * 0.01 - 0.1 * job_remaining_times[job_id]

                if cost < min_cost:
                    min_cost = cost
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            machine_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job_id] = best_start_time + best_processing_time
            job_remaining_times[job_id] -= best_processing_time
            machine_load[best_machine] += best_processing_time


            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

    return schedule
