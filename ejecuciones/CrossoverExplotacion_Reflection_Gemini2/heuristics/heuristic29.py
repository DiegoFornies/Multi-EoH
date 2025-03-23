
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes minimizing idle time and balancing machine load.
    It iterates through jobs and operations, assigning operations to machines that minimize the completion time,
    considering both machine availability and job precedence.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}

    for job_id in jobs:
        schedule[job_id] = []
        for operation_index, operation_data in enumerate(jobs[job_id]):
            available_machines = operation_data[0]
            processing_times = operation_data[1]
            operation_number = operation_index + 1

            best_machine = -1
            min_completion_time = float('inf')

            for machine_index, machine_id in enumerate(available_machines):
                completion_time = max(machine_available_time[machine_id], job_completion_time[job_id]) + processing_times[machine_index]
                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine_id
                    best_processing_time = processing_times[machine_index]

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
    return schedule
