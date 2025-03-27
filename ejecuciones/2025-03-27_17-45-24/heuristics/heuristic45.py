
def heuristic(input_data):
    """Schedules jobs with predictive load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    # Predict future machine load when scheduling.

    for job in jobs:
        schedule[job] = []
        job_completion_time = 0

        for op_idx, operation in enumerate(jobs[job]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_finish_time = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                available_time = max(machine_available_time[machine], job_completion_time)
                finish_time = available_time + processing_time

                #Predictive load balancing
                future_load = 0
                for future_job in jobs:
                    if future_job != job:
                        for future_op_idx in range(len(jobs[future_job])):
                            future_operation = jobs[future_job][future_op_idx]
                            future_machines, future_times = future_operation
                            if machine in future_machines:
                                future_m_idx = future_machines.index(machine)
                                future_load += future_times[future_m_idx]

                #Adjusted finish time incorporates future machine load
                adjusted_finish_time = finish_time + 0.001*future_load
                if adjusted_finish_time < min_finish_time:
                    min_finish_time = adjusted_finish_time
                    best_machine = machine
                    best_start_time = available_time
                    best_processing_time = processing_time

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
