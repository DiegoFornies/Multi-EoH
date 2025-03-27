
def heuristic(input_data):
    """
    Combines SPT and machine idle time to balance makespan and workload.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    machine_assignments = {m: [] for m in range(n_machines)}

    for job_id in jobs:
        schedule[job_id] = []
        current_time = 0

        for op_idx, operation in enumerate(jobs[job_id]):
            possible_machines = operation[0]
            possible_times = operation[1]

            best_machine = None
            min_end_time = float('inf')
            shortest_processing_time = float('inf')

            # Heuristic: Find machine with shortest processing time and earliest availability
            for i, machine_id in enumerate(possible_machines):
                processing_time = possible_times[i]
                available_time = machine_available_times[machine_id]
                start_time = max(available_time, job_completion_times[job_id])
                end_time = start_time + processing_time

                if processing_time < shortest_processing_time:
                    shortest_processing_time = processing_time
                    min_end_time = end_time
                    best_machine = machine_id
                elif processing_time == shortest_processing_time and end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine_id

            processing_time = possible_times[possible_machines.index(best_machine)]
            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time
            machine_assignments[best_machine].append(job_id)
            current_time = end_time

    return schedule
