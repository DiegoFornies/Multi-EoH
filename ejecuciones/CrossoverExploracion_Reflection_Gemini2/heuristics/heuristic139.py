
def heuristic(input_data):
    """
    A heuristic to solve the FJSSP.
    Combines SPT, earliest machine availability, and load balancing.
    Dynamically adapts by prioritizing machines with lower average loads.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    job_current_operation = {j: 1 for j in jobs_data}

    operations = []
    for job_id, job in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx + 1,
                'machines': machines,
                'times': times
            })

    def calculate_machine_load(machine):
        total_load = 0
        for job_schedule in schedule.values():
            for scheduled_op in job_schedule:
                if scheduled_op['Assigned Machine'] == machine:
                    total_load += scheduled_op['Processing Time']
        return total_load

    def calculate_average_machine_load():
        total_loads = [calculate_machine_load(m) for m in range(n_machines)]
        return sum(total_loads) / n_machines if n_machines > 0 else 0

    def prioritize_load_balancing(machines, times):
        average_load = calculate_average_machine_load()
        machine_scores = []

        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]
            machine_load = calculate_machine_load(machine)
            # Prioritize machines with load less than or equal to the average load.
            if machine_load <= average_load:
                machine_scores.append((machine, time, average_load - machine_load))  # Smaller difference is better
            else:
                machine_scores.append((machine, time, -1)) #Penalize those machines

        machine_scores = sorted([ms for ms in machine_scores if ms[2] > -1], key=lambda x: x[2], reverse = True)
        valid_machines = [m[0] for m in machine_scores]
        valid_times = [t[1] for t in machine_scores]

        if valid_machines:
            return valid_machines, valid_times
        else: #No machine under loaded, return original ones
            return machines, times

    available_operations = [op for op in operations if op['op_idx'] == job_current_operation[op['job_id']]]

    while available_operations:
        available_operations.sort(key=lambda op: min(op['times']))

        operation = available_operations.pop(0)

        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        #Load balancing
        machines, times = prioritize_load_balancing(machines, times)

        best_machine = None
        min_end_time = float('inf')
        processing_time = None

        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]

            available_time = machine_available_time[machine]
            start_time = max(available_time, job_completion_time[job_id])
            end_time = start_time + time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = time

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_idx,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

        job_current_operation[job_id] += 1
        available_operations = [op for op in operations if op['op_idx'] == job_current_operation[op['job_id']]]
        new_available_operations = []
        for op in operations:
            if op['op_idx'] == job_current_operation[op['job_id']]:
                is_scheduled = False
                for job_schedule in schedule.values():
                    for scheduled_op in job_schedule:
                        if scheduled_op['Operation'] == op['op_idx'] and scheduled_op['Assigned Machine']:
                            is_scheduled = True
                            break
                    if is_scheduled:
                        break
                if not is_scheduled:
                    new_available_operations.append(op)
        available_operations = new_available_operations

    return schedule
