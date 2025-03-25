
def heuristic(input_data):
    """
    A heuristic to solve the FJSSP, prioritizing machines with earliest availability
    and minimizing idle time between operations.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        for operation_index, operation_data in enumerate(jobs_data[job_id]):
            machines, processing_times = operation_data
            operation_number = operation_index + 1

            best_machine = None
            min_end_time = float('inf')

            for machine_index, machine_id in enumerate(machines):
                processing_time = processing_times[machine_index]
                start_time = max(machine_available_time[machine_id], job_end_time[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine_id
                    best_start_time = start_time
                    best_processing_time = processing_time

            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_end_time[job_id] = best_start_time + best_processing_time

            schedule[job_id].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

    return schedule
