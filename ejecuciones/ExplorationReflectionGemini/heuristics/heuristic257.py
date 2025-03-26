
def heuristic(input_data):
    """A dispatching rule-based heuristic for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        job_operations = jobs[job_id]

        for operation_index, operation_data in enumerate(job_operations):
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            #Earliest Due Date(EDD) dispatching rule
            due_date = sum([sum(op[1]) for op in jobs[job_id][operation_index:]])
            
            # Shortest Processing Time(SPT) dispatching rule
            spt_machine = None
            spt_cost = float('inf')

            for i, machine in enumerate(possible_machines):
                processing_time = possible_times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time
                if processing_time < spt_cost:
                    spt_cost = processing_time
                    spt_machine = machine
                    spt_start_time = start_time
                    spt_processing_time = processing_time

            schedule[job_id].append({
                'Operation': operation_index + 1,
                'Assigned Machine': spt_machine,
                'Start Time': spt_start_time,
                'End Time': spt_start_time + spt_processing_time,
                'Processing Time': spt_processing_time
            })

            machine_available_times[spt_machine] = spt_start_time + spt_processing_time
            job_completion_times[job_id] = spt_start_time + spt_processing_time

    return schedule
