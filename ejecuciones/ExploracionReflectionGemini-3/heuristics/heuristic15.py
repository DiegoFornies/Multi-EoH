
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes shorter processing times and available machines.
    It aims to minimize makespan and balance machine load by assigning operations to the
    earliest available machine with the shortest processing time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    schedule = {}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        operation_number = 1
        for operation_machines, operation_times in jobs[job]:
            best_machine, best_time = -1, float('inf')
            earliest_start = float('inf')
            selected_processing_time = -1

            for i, machine in enumerate(operation_machines):
                processing_time = operation_times[i]
                available_time_on_machine = machine_available_times[machine]
                start_time = max(available_time_on_machine, job_completion_times[job])

                if start_time < earliest_start or (start_time == earliest_start and processing_time < best_time):
                    earliest_start = start_time
                    best_machine = machine
                    best_time = processing_time
                    selected_processing_time = processing_time

            start_time = earliest_start
            end_time = start_time + selected_processing_time

            schedule[job].append({
                'Operation': operation_number,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': selected_processing_time
            })

            machine_available_times[best_machine] = end_time
            job_completion_times[job] = end_time
            operation_number += 1

    return schedule
