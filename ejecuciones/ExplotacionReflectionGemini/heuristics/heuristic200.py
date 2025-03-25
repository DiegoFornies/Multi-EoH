
def heuristic(input_data):
    """FJSSP heuristic: SPT with load balancing, then local search."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Phase 1: SPT with Load Balancing
    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append((job_id, 0))

    scheduled_operations = set()

    while available_operations:
        best_operation = None
        best_machine = None
        min_completion_time = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]

            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                start_time = max(machine_load[machine], job_completion_time[job_id])
                completion_time = start_time + processing_time

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_operation = (job_id, op_idx)
                    best_machine = (machine, processing_time)

        job_id, op_idx = best_operation
        machine, processing_time = best_machine

        start_time = max(machine_load[machine], job_completion_time[job_id])
        end_time = start_time + processing_time
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_load[machine] = end_time
        job_completion_time[job_id] = end_time
        available_operations.remove((job_id, op_idx))

        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))

    # Phase 2: Local Search (Operation Swaps for Balance)
    def calculate_machine_load(sched):
        machine_load_values = {m: 0 for m in range(n_machines)}
        for job_id in sched:
            for op in sched[job_id]:
                machine = op['Assigned Machine']
                machine_load_values[machine] = max(machine_load_values[machine], op['End Time'])
        return machine_load_values

    def calculate_balance(machine_load_values):
        total_load = sum(machine_load_values.values())
        if not machine_load_values:
            return 0  # Avoid division by zero if there are no machines
        num_machines = len(machine_load_values)
        average_load = total_load / num_machines
        squared_diffs = [(load - average_load) ** 2 for load in machine_load_values.values()]
        variance = sum(squared_diffs) / num_machines
        return variance # Lower variance means better balance


    original_balance = calculate_balance(calculate_machine_load(schedule))

    for _ in range(500):  # Iterations of local search
        # Randomly select two jobs and two operations within those jobs
        job1 = int(n_jobs * (0.5 + 0.5 * (hash(_ * 111 %1000 + 1234567) % 2000 - 1000)/ 1000)) % n_jobs + 1
        job2 = int(n_jobs * (0.5 + 0.5 * (hash(_ * 222 % 1000+7654321) % 2000 - 1000)/ 1000)) % n_jobs + 1

        if len(schedule[job1]) < 1 or len(schedule[job2]) < 1:
            continue  # Skip if jobs have no operations
        op_index1 = int(len(schedule[job1]) * (0.5 + 0.5 * (hash(_ * 333 % 1000 + 9876543) % 2000 - 1000)/ 1000)) % len(schedule[job1])
        op_index2 = int(len(schedule[job2]) * (0.5 + 0.5 * (hash(_ * 444 % 1000+3456789) % 2000 - 1000)/ 1000)) % len(schedule[job2])

        #Ensure op_index are not None and that both jobs have operations to swap.
        if op_index1 is None or op_index2 is None:
            continue


        # Swap the assigned machines and processing times
        original_machine1 = schedule[job1][op_index1]['Assigned Machine']
        original_machine2 = schedule[job2][op_index2]['Assigned Machine']

        schedule[job1][op_index1]['Assigned Machine'], schedule[job2][op_index2]['Assigned Machine'] = original_machine2, original_machine1

        # Re-evaluate start and end times based on the updated assigned machines
        machine_load = {m: 0 for m in range(n_machines)}
        job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
        temp_schedule = {j: [] for j in range(1, n_jobs + 1)}

        for job_id in range(1, n_jobs + 1):
            for op_idx in range(len(schedule[job_id])):
                assigned_machine = schedule[job_id][op_idx]['Assigned Machine']

                processing_time = None
                machines, times = jobs[job_id][op_idx]
                for mach_idx, mach in enumerate(machines):
                    if mach == assigned_machine:
                        processing_time = times[mach_idx]
                        break

                start_time = max(machine_load[assigned_machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                temp_schedule[job_id].append({
                    'Operation': op_idx + 1,
                    'Assigned Machine': assigned_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })

                machine_load[assigned_machine] = end_time
                job_completion_time[job_id] = end_time

        # Check if the swap improved the balance
        new_balance = calculate_balance(calculate_machine_load(temp_schedule))

        if new_balance < original_balance: #Improved schedule found:
            schedule = temp_schedule
            original_balance = new_balance
        else:  # Revert the swap if it didn't improve balance
            schedule[job1][op_index1]['Assigned Machine'], schedule[job2][op_index2]['Assigned Machine'] = original_machine1, original_machine2

    return schedule
