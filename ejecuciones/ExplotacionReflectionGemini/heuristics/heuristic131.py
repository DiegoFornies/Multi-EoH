
def heuristic(input_data):
    """Combines machine load and operation time for FJSSP scheduling."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    solution = {}
    for job_id in jobs:
        solution[job_id] = []

    for job_id, operations in jobs.items():
        for op_idx, op_data in enumerate(operations):
            machines, times = op_data
            op_num = op_idx + 1

            best_machine = None
            min_end_time = float('inf')
            best_processing_time = None

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]

                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time

            solution[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time

    return solution
