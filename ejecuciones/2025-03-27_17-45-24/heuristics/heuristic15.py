
def heuristic(input_data):
    """Schedules jobs minimizing idle time and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs}
    schedule = {}

    # Prioritize jobs with more operations (Longest Processing Time first).
    job_priorities = sorted(jobs.keys(), key=lambda job: len(jobs[job]), reverse=True)

    for job in job_priorities:
        schedule[job] = []
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1
            best_machine, best_start_time, best_processing_time = None, float('inf'), None

            # Iterate through available machines for this operation
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                available_time = machine_available_times[machine]
                job_ready_time = job_completion_times[job]

                # Calculate start time (respecting machine and job constraints).
                start_time = max(available_time, job_ready_time)

                # Minimize start time and Machine Load to balance load and reduce makespan.
                if start_time < best_start_time:
                    best_machine, best_start_time, best_processing_time = machine, start_time, processing_time
                elif start_time == best_start_time and machine_load[machine] < machine_load[best_machine if best_machine is not None else machines[0]]:
                     best_machine, best_start_time, best_processing_time = machine, start_time, processing_time

            # Schedule operation on the best machine
            start_time = best_start_time
            end_time = start_time + best_processing_time
            machine_available_times[best_machine] = end_time
            job_completion_times[job] = end_time
            machine_load[best_machine] += best_processing_time # update machine load

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

    return schedule
