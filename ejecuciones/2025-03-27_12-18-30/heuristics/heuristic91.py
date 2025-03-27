
def heuristic(input_data):
    """Schedules jobs balancing start time, machine load, and job complexity."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_priority = sorted(jobs.keys(), key=lambda job_id: len(jobs[job_id]), reverse=True)

    for job in job_priority:
        schedule[job] = []
        job_completion_time = 0

        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            best_machine = None
            earliest_end_time = float('inf')
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time)
                end_time = start_time + processing_time
                load_factor = machine_load[machine]

                if end_time < earliest_end_time:
                    earliest_end_time = end_time
                    best_machine = machine
                    best_processing_time = processing_time
                elif end_time == earliest_end_time and load_factor < machine_load.get(best_machine, float('inf')):
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = max(machine_available_time[best_machine], job_completion_time)
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += best_processing_time
            job_completion_time = end_time

    return schedule
