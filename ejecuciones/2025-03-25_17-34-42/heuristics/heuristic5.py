
def heuristic(input_data):
    """
    A heuristic scheduling algorithm for FJSSP that prioritizes minimizing idle time and balancing machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    machine_assignments = {m: [] for m in range(n_machines)}

    schedule = {}

    for job_id in jobs:
        schedule[job_id] = []
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            op_num = op_idx + 1

            # Find the machine that minimizes the completion time of the operation
            best_machine = None
            min_completion_time = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                completion_time = start_time + processing_time

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine
                    best_processing_time = processing_time

            # Assign the operation to the best machine
            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine and job completion times
            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time
            machine_assignments[best_machine].append((job_id, op_num))

    return schedule
