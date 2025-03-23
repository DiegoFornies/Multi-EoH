
def heuristic(input_data):
    """Schedules jobs minimizing makespan and improving separation."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_workload = {m: 0 for m in range(n_machines)}

    ready_operations = []
    for job_id, operations in jobs_data.items():
        ready_operations.append((job_id, 0))

    while ready_operations:
        best_job, best_op_index = None, None
        earliest_start_time = float('inf')

        for job_id, op_index in ready_operations:
            machines, times = jobs_data[job_id][op_index]

            min_start_time = float('inf')
            for machine_id, processing_time in zip(machines, times):
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                min_start_time = min(min_start_time, start_time)

            if min_start_time < earliest_start_time:
                earliest_start_time = min_start_time
                best_job, best_op_index = job_id, op_index

        job_id, op_index = best_job, best_op_index
        machines, times = jobs_data[job_id][op_index]

        # Select machine with shortest processing time AND least workload, incorporating separation.
        best_machine, best_processing_time = None, float('inf')
        min_combined_score = float('inf')

        for m_idx, machine_id in enumerate(machines):
            processing_time = times[m_idx]
            available_time = machine_available_times[machine_id]
            start_time = max(available_time, job_completion_times[job_id])
            end_time = start_time + processing_time

            # Separation heuristic: Delay start if other jobs are about to finish on other machines.
            separation_delay = 0
            for other_job_id in range(1, n_jobs + 1):
                if other_job_id != job_id and schedule[other_job_id]:
                    last_op = schedule[other_job_id][-1]
                    if last_op['End Time'] < end_time:  #Consider finish time
                        separation_delay = max(0, end_time - last_op['End Time'])  #Delay proportional to overlap

            combined_score = end_time + machine_workload[machine_id]*0.001 + separation_delay*0.01
            #separation_delay is weighted significantly lower

            if combined_score < min_combined_score:
                min_combined_score = combined_score
                best_machine = machine_id
                best_processing_time = processing_time
                best_start_time = start_time

        start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
        end_time = start_time + best_processing_time
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_workload[best_machine] += best_processing_time

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        ready_operations.remove((job_id, op_index))

        if op_index + 1 < len(jobs_data[job_id]):
            ready_operations.append((job_id, op_index + 1))

    return schedule
