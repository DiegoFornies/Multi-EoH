
def heuristic(input_data):
    """Heuristic: Iterative Bottleneck Shifting."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    scheduled_operations = {} # track op scheduling details
    
    for job_id in range(1, n_jobs + 1):
        schedule[job_id] = []
        scheduled_operations[job_id] = {}

    def calculate_makespan(current_schedule):
        completion_times = {}
        for job_id in current_schedule:
            if current_schedule[job_id]:
                completion_times[job_id] = current_schedule[job_id][-1]['End Time']
            else:
                completion_times[job_id] = 0 # Handle empty schedules
        return max(completion_times.values()) if completion_times else 0

    def initial_schedule():
        """Create initial schedule based on shortest processing time"""
        machine_available_times = {m: 0 for m in range(n_machines)}
        job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
        schedule = {}
        for job_id in range(1, n_jobs + 1):
            schedule[job_id] = []
            job_operations = jobs[job_id]

            for operation_index, operation_data in enumerate(job_operations):
                possible_machines = operation_data[0]
                possible_times = operation_data[1]

                best_machine = None
                min_time = float('inf')
                for i, machine in enumerate(possible_machines):
                    if possible_times[i] < min_time:
                        min_time = possible_times[i]
                        best_machine = machine
                        processing_time = possible_times[i]

                start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                schedule[job_id].append({
                    'Operation': operation_index + 1,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })

                machine_available_times[best_machine] = end_time
                job_completion_times[job_id] = end_time
        return schedule

    current_schedule = initial_schedule()
    best_schedule = current_schedule
    best_makespan = calculate_makespan(current_schedule)

    # Iterate for a limited number of iterations
    for _ in range(10):  # Adjust the number of iterations as needed

        # Find bottleneck machine (machine with highest load)
        machine_load = {m: 0 for m in range(n_machines)}
        for job_id in current_schedule:
            for operation in current_schedule[job_id]:
                machine_load[operation['Assigned Machine']] += operation['Processing Time']
        bottleneck_machine = max(machine_load, key=machine_load.get)

        # Reschedule operations on the bottleneck machine

        # Collect all operations processed on the bottleneck machine
        bottleneck_operations = []
        for job_id in range(1, n_jobs + 1):
          for op_index, operation in enumerate(current_schedule[job_id]):
            if operation['Assigned Machine'] == bottleneck_machine:
                bottleneck_operations.append((job_id, op_index))

        # Try rescheduling each operation on the bottleneck machine
        for job_id, op_index in bottleneck_operations:
            original_machine = current_schedule[job_id][op_index]['Assigned Machine']
            original_start_time = current_schedule[job_id][op_index]['Start Time']
            original_end_time = current_schedule[job_id][op_index]['End Time']
            original_processing_time = current_schedule[job_id][op_index]['Processing Time']
            
            operation_data = jobs[job_id][op_index]
            possible_machines = operation_data[0]
            possible_times = operation_data[1]

            # Find alternative machines and times
            alternative_machines = []
            alternative_times = []
            for i, machine in enumerate(possible_machines):
                if machine != original_machine:
                    alternative_machines.append(machine)
                    alternative_times.append(possible_times[i])

            if not alternative_machines:
                continue # No alternative machines

            # Evaluate alternative machines based on makespan
            for i, alternative_machine in enumerate(alternative_machines):
                temp_schedule = {}
                for j in range(1, n_jobs + 1):
                    temp_schedule[j] = current_schedule[j][:]
                
                processing_time = alternative_times[i]
                
                
                #Attempt to reschedule the operation
                
                # Remove the old schedule entry of the operation.

                start_time = 0
                if op_index > 0:
                    start_time = temp_schedule[job_id][op_index-1]['End Time']
                start_time = max(start_time, machine_available_times.get(alternative_machine, 0))

                end_time = start_time + processing_time

                # Create new operation entry
                new_operation = {
                    'Operation': op_index + 1,
                    'Assigned Machine': alternative_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                }
                temp_schedule[job_id][op_index] = new_operation
                
                
                makespan = calculate_makespan(temp_schedule)

                #If the make span is better
                if makespan < best_makespan:
                    best_makespan = makespan
                    best_schedule = temp_schedule
    return best_schedule
