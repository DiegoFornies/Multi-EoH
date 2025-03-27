
def heuristic(input_data):
    """Schedules jobs considering machine workload and job urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    job_urgency = {}
    for job_id in jobs:
        job_urgency[job_id] = sum(min(op[1]) for op in jobs[job_id])

    for job_id in sorted(jobs.keys(), key=lambda x: job_urgency[x]):
        schedule[job_id] = []
        for op_idx, operation in enumerate(jobs[job_id]):
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_end_time = float('inf')

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                load_increase = processing_time
                future_load = machine_load[machine] + load_increase

                #Prioritize machines with less load, considering immediate and future impact.
                if end_time + future_load*0.1 < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
            
            if best_machine is None: #Handle edge case
                best_machine = machines[0]
                processing_time = times[0]
                start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
                end_time = start_time + processing_time

            processing_time = times[machines.index(best_machine)] if best_machine in machines else times[0]
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += processing_time
            job_completion_time[job_id] = end_time

    return schedule
