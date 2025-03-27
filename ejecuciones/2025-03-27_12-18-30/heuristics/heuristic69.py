
def heuristic(input_data):
    """Schedules jobs using Shortest Processing Time (SPT) and load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job_completion_time = 0

        for op_idx, op_data in enumerate(jobs[job_id]):
            machines, times = op_data
            op_num = op_idx + 1

            best_machine = None
            min_makespan = float('inf')

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time)
                end_time = start_time + processing_time
                makespan = end_time  #Consider Makespan

                if makespan < min_makespan:
                    min_makespan = makespan
                    best_machine = machine
                    best_processing_time = processing_time

            if best_machine is not None:
                start_time = max(machine_available_time[best_machine], job_completion_time)
                end_time = start_time + best_processing_time

                schedule[job_id].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': best_processing_time
                })

                machine_available_time[best_machine] = end_time
                machine_load[best_machine] += best_processing_time
                job_completion_time = end_time
            else:
                return None

    return schedule
