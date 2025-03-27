
def heuristic(input_data):
    """FJSSP heuristic: Schedules jobs using a shortest processing time and earliest finish time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}

    for job in jobs:
        schedule[job] = []
        job_completion_time = 0

        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            # Shortest processing time and earliest finish time
            best_machine = None
            min_finish_time = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time)
                finish_time = start_time + processing_time

                if finish_time < min_finish_time:
                    min_finish_time = finish_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            # Schedule
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_start_time + best_processing_time
            job_completion_time = best_start_time + best_processing_time

    return schedule
