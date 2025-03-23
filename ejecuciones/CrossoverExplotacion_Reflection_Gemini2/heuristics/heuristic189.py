
def heuristic(input_data):
    """Hybrid heuristic: SPT, machine load, job dependency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available = {m: 0 for m in range(n_machines)}
    job_completion = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        best_machine, best_processing_time = None, float('inf')
        earliest_finish = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available[machine], job_completion[job_id])
                end_time = start_time + processing_time

                workload = machine_load[machine]

                weighted_finish = 0.7 * end_time + 0.3 * workload
                #Consider job wait time from the parent to reduce idle time between operations
                if weighted_finish < earliest_finish:
                    earliest_finish = weighted_finish
                    best_job, best_op_index = job_id, op_index
                    best_machine, best_processing_time = processing_time
        job_id, op_index = best_job, best_op_index
        start_time = max(machine_available[best_machine], job_completion[job_id])
        end_time = start_time + best_processing_time
        
        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available[best_machine] = end_time
        job_completion[job_id] = end_time
        machine_load[best_machine] += best_processing_time

        ready_operations.remove((job_id, op_index))
        if op_index + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_index + 1))

    return schedule
