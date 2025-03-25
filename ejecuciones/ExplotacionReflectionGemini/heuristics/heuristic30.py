
def heuristic(input_data):
    """A heuristic for FJSSP: schedules operations greedily, prioritizing shortest processing time and earliest available machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        for operation_index, operation in enumerate(jobs_data[job_id]):
            machines, processing_times = operation
            
            best_machine, best_start_time, best_processing_time = None, float('inf'), None

            for machine_index, machine in enumerate(machines):
                processing_time = processing_times[machine_index]
                available_time = machine_available_times[machine]
                start_time = max(available_time, job_completion_times[job_id])

                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_processing_time = processing_time
            
            start_time = best_start_time
            end_time = start_time + best_processing_time
            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

    return schedule
