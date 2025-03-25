
def heuristic(input_data):
    """Schedules operations based on earliest finish time and load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {}

    for job_id in jobs:
        schedule[job_id] = []
        for operation_index, operation_data in enumerate(jobs[job_id]):
            available_machines = operation_data[0]
            processing_times = operation_data[1]

            best_machine = None
            min_end_time = float('inf')
            best_processing_time = 0
            best_start_time = 0

            for i, machine_id in enumerate(available_machines):
                processing_time = processing_times[i]
                start_time = max(machine_available_time[machine_id], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine_id
                    best_processing_time = processing_time
                    best_start_time = start_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_start_time + best_processing_time
            machine_load[best_machine] += best_processing_time
            job_completion_time[job_id] = best_start_time + best_processing_time

    return schedule
