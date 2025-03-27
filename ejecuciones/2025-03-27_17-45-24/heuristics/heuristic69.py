
def heuristic(input_data):
    """Schedules jobs using a Shortest Processing Time and Earliest Finish Time heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    for job in range(1, n_jobs + 1):
        schedule[job] = []
        for op_idx, operation in enumerate(jobs_data[job]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_finish_time = float('inf')
            shortest_processing_time = float('inf')

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                finish_time = start_time + processing_time

                if processing_time < shortest_processing_time:
                    shortest_processing_time = processing_time
                    min_finish_time = finish_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

                elif processing_time == shortest_processing_time and finish_time < min_finish_time:
                    min_finish_time = finish_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            if best_machine is not None:
                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': best_start_time,
                    'End Time': best_start_time + best_processing_time,
                    'Processing Time': best_processing_time
                })

                machine_available_time[best_machine] = best_start_time + best_processing_time
                job_completion_time[job] = best_start_time + best_processing_time

    return schedule
