
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes minimizing machine idle time
    and considers operation duration when assigning machines.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_loads = {m: 0 for m in range(n_machines)}  # Track machine workload

    for job_id in jobs:
        schedule[job_id] = []
        job_completion_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_end_time = float('inf')

            # Find the machine that minimizes completion time,
            # considering both machine availability and machine load.

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time)
                end_time = start_time + processing_time

                # Prioritize machines with lower load. If loads are equal, minimize end time.
                if end_time < min_end_time or (end_time == min_end_time and machine_loads[machine] < machine_loads[best_machine] if best_machine is not None else False):
                    best_machine = machine
                    min_end_time = end_time
                    best_processing_time = processing_time

            # Schedule the operation on the best machine
            start_time = max(machine_available_time[best_machine], job_completion_time)
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job completion times
            machine_available_time[best_machine] = end_time
            machine_loads[best_machine] += best_processing_time # Update the machine load
            job_completion_time = end_time

    return schedule
