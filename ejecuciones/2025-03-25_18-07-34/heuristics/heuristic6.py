
def heuristic(input_data):
    """
    A heuristic for the FJSSP that considers machine workload when assigning operations.
    It prioritizes assigning operations to the least loaded machines.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}  # Keep track of machine workload
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}  # Completion times of jobs

    for job_id in jobs:
        schedule[job_id] = []
        job_ops = jobs[job_id]
        current_job_time = 0

        for op_idx, op_data in enumerate(job_ops):
            machines, times = op_data
            op_num = op_idx + 1

            # Find the machine with the least load among the available machines
            available_machines_loads = {m: machine_load[m] for m in machines}
            best_machine = min(available_machines_loads, key=available_machines_loads.get)

            # Get the processing time for the chosen machine
            processing_time = times[machines.index(best_machine)]

            # Schedule the operation on the chosen machine
            start_time = max(machine_load[best_machine], current_job_time)  # Avoid machine overlap, sequence feasibility
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine load and job completion time
            machine_load[best_machine] = end_time
            current_job_time = end_time

    return schedule
