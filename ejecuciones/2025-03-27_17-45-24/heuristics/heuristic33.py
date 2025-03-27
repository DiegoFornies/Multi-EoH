
def heuristic(input_data):
    """Heuristic: SPT+LPT Hybrid for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}

    # SPT: Sort jobs by total processing time (shortest first)
    job_processing_times = {}
    for job_id, operations in jobs.items():
        total_time = sum(min(op[1]) for op in operations)
        job_processing_times[job_id] = total_time

    sorted_jobs = sorted(jobs.keys(), key=lambda job_id: job_processing_times[job_id])

    #LPT: Sort operation in job by longest processing time first
    for job_id in sorted_jobs:
        schedule[job_id] = []
        operations = jobs[job_id]

        #Sort operation by LPT
        operation_processing_time = {}
        for op_idx, operation in enumerate(operations):
            operation_processing_time[op_idx] = max(operation[1])
        operation_indices = sorted(operation_processing_time,key=operation_processing_time.get,reverse=True)

        for op_idx in operation_indices:
            operation = jobs[job_id][op_idx]
            machines, times = operation
            op_num = op_idx + 1

            best_machine = None
            min_end_time = float('inf')

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_available_time[machine],
                                 schedule[job_id][-1]['End Time'] if op_idx > 0 and schedule[job_id] else 0)
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine

            if best_machine is None:
                best_machine = machines[0]
                processing_time = times[0]
                start_time = max(machine_available_time[best_machine],
                                 schedule[job_id][-1]['End Time'] if op_idx > 0 and schedule[job_id] else 0)
                end_time = start_time + processing_time

            processing_time = times[machines.index(best_machine)] if best_machine in machines else times[0]
            start_time = max(machine_available_time[best_machine],
                             schedule[job_id][-1]['End Time'] if op_idx > 0 and schedule[job_id] else 0)
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time

    return schedule
