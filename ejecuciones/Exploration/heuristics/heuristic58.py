
def heuristic(input_data):
    """Schedule by shortest processing time (SPT) on least loaded machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_loads = {m: 0 for m in range(n_machines)}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in jobs:
        schedule[job_id] = []
        for op_idx, operation in enumerate(jobs[job_id]):
            machines = operation[0]
            processing_times = operation[1]
            op_num = op_idx + 1

            # Find the machine with the shortest processing time and least load
            best_machine = None
            min_pt = float('inf')
            least_load = float('inf')

            for i, machine in enumerate(machines):
                pt = processing_times[i]
                if pt < min_pt or (pt == min_pt and machine_loads[machine] < least_load):
                    min_pt = pt
                    best_machine = machine
                    least_load = machine_loads[machine]
                    best_processing_time = pt

            # Schedule the operation
            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job times
            machine_available_times[best_machine] = end_time
            machine_loads[best_machine] += best_processing_time
            job_completion_times[job_id] = end_time

    return schedule
