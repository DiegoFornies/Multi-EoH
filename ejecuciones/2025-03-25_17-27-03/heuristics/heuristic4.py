
def heuristic(input_data):
    """
    A heuristic for FJSSP scheduling: earliest finish time on least loaded machine.
    Prioritizes machines with less workload to balance utilization.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        current_job_ops = jobs_data[job_id]

        for op_idx, op_data in enumerate(current_job_ops):
            machines, times = op_data

            best_machine = None
            earliest_start_time = float('inf')

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                available_time = machine_available_times[machine]
                job_ready_time = job_completion_times[job_id]

                start_time = max(available_time, job_ready_time)
                finish_time = start_time + processing_time

                if finish_time < earliest_start_time:
                    earliest_start_time = finish_time
                    best_machine = machine
                    best_processing_time = processing_time

            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + best_processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time

    return schedule
