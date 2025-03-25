
def heuristic(input_data):
    """Heuristic for FJSSP: SPT with job sequence priority.
    Chooses machine with earliest finish time for each operation,
    respecting job order."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in jobs:
        schedule[job_id] = []
        for operation_index, operation in enumerate(jobs[job_id]):
            machines, times = operation

            best_machine = None
            min_end_time = float('inf')
            best_processing_time = None
            best_start_time = None

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time

            operation_number = operation_index + 1
            schedule[job_id].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time[job_id] = best_start_time + best_processing_time

    return schedule
