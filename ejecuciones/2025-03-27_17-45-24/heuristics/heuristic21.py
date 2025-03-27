
def heuristic(input_data):
    """Aims to minimize makespan using a greedy approach with machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id in jobs:
        schedule[job_id] = []
        current_job_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            op_num = op_idx + 1

            # Find the best machine based on availability and load
            best_machine = None
            min_end_time = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], current_job_time)
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time #added to fix process_time error

            # Schedule the operation on the best machine
            start_time = max(machine_available_time[best_machine], current_job_time)
            end_time = start_time + best_processing_time # Fixed the process_time
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            # Update machine availability and job time
            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += best_processing_time
            current_job_time = end_time

    return schedule
