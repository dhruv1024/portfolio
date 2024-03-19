import time
import pickle
import os
import configparser
import msvcrt
from gtts import gTTS
import tempfile
import threading

import pygame
import sounddevice as sd

#from playsound import playsound
#from pydub import AudioSegment, play
#import subprocess

# Load tasks from config file
config = configparser.ConfigParser()
config.read("tasks.ini")

tasks = []
sub_task_status_config = configparser.ConfigParser()
sub_task_status_config.read("sub_task_statuses.ini")

# Create the directory if it doesn't exist
#permanent_audio_directory = "TaskMaster_audio"
#if not os.path.exists(permanent_audio_directory):
#    os.makedirs(permanent_audio_directory)

for section in config.sections():
    if config.has_option(section, "Description"):
        task = {
            "stage": section,
            "description": config[section]["Description"],
            "start_date": config[section]["Start_Date"],
            "deadline": config[section]["Deadline"],
            "status": config[section].get("Status", "Pending"),  # Default to "Pending" if not specified
            "time_estimate": int(config[section]["Estimated_Time_Minutes"]) * 60,
            "reward_points": 0,
            "xp": 0,
            "level": 1,
            "sub_tasks": []
        }

        stage = section.replace(' ', '-').replace('/', '-')
        sub_task_section = f"Sub_Tasks_{stage}"  # Use a sub-section for sub-tasks
        if sub_task_section in config: 
            for key in config[sub_task_section]:
                sub_task_description = config[sub_task_section][key]
                sub_task_status_key = f"Sub_Task_Status_{key.split('_')[-1]}"
                # what key is used? above is reading from main ini
                sub_task_status = sub_task_status_config[sub_task_section][sub_task_status_key]
                task["sub_tasks"].append({"description": sub_task_description, "completed": sub_task_status == "Completed"})

        tasks.append(task)

# Initialize a timer
start_time = None
show_help = False

# Visual Theming
# Total number of ladder steps
LADDER_STEPS = sum(1 for task in tasks if task["status"] == "Pending") #LADDER_STEPS = 5  
SPACE_ADVENTURE_THEME = {
    "ladder": "🚀",
    "alien": "👾",
    "alien_color": "\033[91m",  # Red
    "reset_color": "\033[0m"    # Reset color
}

# Function to calculate task progress based on sub-tasks
def calculate_task_progress(task):
    total_sub_tasks = len(task.get("sub_tasks", []))
    completed_sub_tasks = sum(1 for sub_task in task.get("sub_tasks", []) if sub_task.get("completed", False))
    return completed_sub_tasks / total_sub_tasks if total_sub_tasks > 0 else 1.0

def mark_sub_task_complete(task):
    print("Sub-tasks:")
    for idx, sub_task in enumerate(task['sub_tasks'], start=1):
        sub_task_status = "Completed" if sub_task.get("completed", False) else "Pending"
        print(f"{idx}. {sub_task['description']} - {sub_task_status}")

    sub_task_index = int(input("Enter the index of the sub-task to mark as complete (or 0 to cancel): "))

    sub_task_section = f"Sub_Tasks_{task['stage'].replace(' ', '-').replace('/', '-')}"
    sub_task_key = f"Sub_Task_{sub_task_index}"
    sub_task_status_key = f"Sub_Task_Status_{sub_task_index}"

    if sub_task_index > 0 and sub_task_index <= len(task['sub_tasks']):
        sub_task = task['sub_tasks'][sub_task_index - 1]
        sub_task['completed'] = True
        sub_task_description = sub_task['description']

        # Update sub-task status in the 'tasks.ini' file
        if sub_task_section not in sub_task_status_config:
            sub_task_status_config[sub_task_section] = {}

        sub_task_status_config[sub_task_section][sub_task_status_key] = "Completed"

        with open("sub_task_statuses.ini", "w") as sub_task_status_file:
            sub_task_status_config.write(sub_task_status_file)

        # Update the 'sub_tasks' list in memory
        task['sub_tasks'][sub_task_index - 1]['completed'] = True
        sub_task_description = task['sub_tasks'][sub_task_index - 1]['description']

        print(f"Sub-task '{sub_task_description}' marked as complete!")
    elif sub_task_index == -1:
        remove_sub_task_index = int(input("Enter the index of the sub-task to remove (or 0 to cancel): "))
        if 0 < remove_sub_task_index <= len(selected_task['sub_tasks']):
            sub_task_to_remove = selected_task['sub_tasks'].pop(remove_sub_task_index - 1)
            print(f"Sub-task '{sub_task_to_remove['description']}' removed!")

            # Remove sub-task entry from 'tasks.ini'
            sub_task_section = f"Sub_Tasks_{selected_task['stage'].replace(' ', '-').replace('/', '-')}"
            sub_task_key = f"Sub_Task_{remove_sub_task_index}"
            if sub_task_key in config[sub_task_section]:
                del config[sub_task_section][sub_task_key]
                with open("tasks.ini", "w") as config_file:
                    config.write(config_file)

            # Remove sub-task status entry from 'sub_task_statuses.ini' (optional, if it exists)
            sub_task_status_key = f"Sub_Task_Status_{remove_sub_task_index}"
            if sub_task_status_key in sub_task_status_config[sub_task_section]:
                del sub_task_status_config[sub_task_section][sub_task_status_key]
                with open("sub_task_statuses.ini", "w") as sub_task_status_file:
                    sub_task_status_config.write(sub_task_status_file)

            if not selected_task['sub_tasks']:
                # If no more sub-tasks, remove sub-task section from 'tasks.ini'
                sub_task_section = f"Sub_Tasks_{selected_task['stage'].replace(' ', '-').replace('/', '-')}"
                if sub_task_section in config:
                    del config[sub_task_section]
                    with open("tasks.ini", "w") as config_file:
                        config.write(config_file)
                        
            if not selected_task['sub_tasks']:
                # If no more sub-tasks, remove sub-task section from 'sub_task_statuses.ini'
                sub_task_section = f"Sub_Tasks_{selected_task['stage'].replace(' ', '-').replace('/', '-')}"
                if sub_task_section in sub_task_status_config:
                    del sub_task_status_config[sub_task_section]
                    with open("sub_task_statuses.ini", "w") as sub_task_status_file:
                        sub_task_status_config.write(sub_task_status_file)

            print("Sub-task removed.")
        else:
            print("Invalid sub-task index.")
# Display the task tracker
def update_header():
    os.system("cls")  # Clear the screen
    # Display mission progress
    completed_projects = sum(1 for task in tasks if task["status"] == "Complete")
    remaining_steps = LADDER_STEPS - completed_projects
    ladder = SPACE_ADVENTURE_THEME["ladder"] * completed_projects
    ladder += SPACE_ADVENTURE_THEME["alien_color"] + SPACE_ADVENTURE_THEME["alien"] * remaining_steps + SPACE_ADVENTURE_THEME["reset_color"]
    
    print("=" * 80)
    print("Mission Progress:")
    indent = int(80/4 + LADDER_STEPS/4)
    print(f"{' '*indent}⇢ {ladder} ⇠")
    if remaining_steps > 0:
        indent = int(80-(len("{remaining_steps} Mission{'s' if remaining_steps > 1 else ''} to Complete!"*3))/4)
        print(f"\033[92m{' '*indent}{remaining_steps} Mission{'s' if remaining_steps > 1 else ''} to Complete!\033[0m")

    # Display upcoming task
    upcoming_task = None
    for task in tasks:
        if task["status"] == "Pending" and task["time_estimate"] > 0:
            upcoming_task = task
            break
    if upcoming_task:
        print(f"\033[91m⇢ New task: {upcoming_task['description']} (Start Date: {upcoming_task['start_date']} | Deadline: {upcoming_task['deadline']})\033[0m")
    else:
        print("No upcoming tasks.")
    print("=" * 80)

pygame.init()
def quit_pygame():
    pygame.mixer.music.stop()
    pygame.mixer.quit()

def play_audio(temp_audio_file):
    pygame.mixer.init()
    pygame.mixer.music.load(temp_audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Control the loop speed

    # abandoned
    # audio_data, _ = sd.read(temp_audio_file, dtype='float32')
    # sd.play(audio_data)
    # sd.wait()

def generate_task_speech(open_tasks):
    text = "Open tasks:"
    for idx, task in enumerate(open_tasks, start=1):
        text += f"\nTask {idx}: {task['description']}"
        if task["sub_tasks"]:
            text += " with sub-tasks:"
            for sub_task in task["sub_tasks"]:
                text += f"\n    - {sub_task['description']}"

    # Create a gTTS object and save it to a temporary file
    tts = gTTS(text)
    
    # using tempfile to reduce clutter
    #temp_audio_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    #temp_audio_file.close()

    temp_audio_file = "temp_audio.mp3"
    tts.save(temp_audio_file)

    #permanent save if we want to use WindowsMedia Player
    #audio_file_name = f"task_{len(open_tasks)}.mp3"
    #audio_file_path = os.path.join(permanent_audio_directory, audio_file_name)
    #tts.save(audio_file_path)

    # Play the generated audio
    #os.system(f"start {temp_audio_file.name}")
    #os.chmod(temp_audio_file.name, 0o755)
    # alternate to os.system(start)
    #subprocess.run(['start', audio_file_path], shell=True)
    
    #playsound library unable to install
    #playsound(temp_audio_file.name)
    
    # pygame audio pausing didn't work correctly
    # pygame.mixer.music.load(temp_audio_file)
    # pygame.mixer.music.play()
    #audio_playing = True

    audio_thread = threading.Thread(target=play_audio, args=(temp_audio_file,))
    audio_thread.start()
    
    # pydub required ffprobe binary download
    #audio = AudioSegment.from_file(temp_audio_file)
    #playback = play(audio)

    # audio_paused = False
    #print("Press 'P' to pause, 'R' to resume, or 'Q' to quit: ")
    print("Press 'K' to kill audio: ")

    while audio_thread.is_alive(): #or audio_paused
        pygame.time.Clock().tick(10)  # Adjust the playback rate if needed
        
        if msvcrt.kbhit():
            user_input = user_input = msvcrt.getch().decode("utf-8").upper()

            # unable to implement pause/unpause. pause exits the loop
            # if user_input == 'P':
            #     if not audio_paused:
            #         pygame.mixer.music.pause()
            #         audio_paused = True
            #         print("Audio paused.")
            #     else:
            #         pygame.mixer.music.unpause()
            #         audio_paused = False
            #         print("Audio resumed.")
            if user_input == 'K':
                pygame.mixer.music.stop()
                #sd.stop()
                print("Audio stopped.")
                break
        
        # Check if audio playback is still ongoing
        # audio_playing = pygame.mixer.music.get_busy() 

    quit_pygame()

    # Clean up the temporary file after playback
    os.remove(temp_audio_file)

current_page = 1
tasks_per_page = 5
show_by_status = False

# Display the task tracker
while True:
    update_header()  # Display header and information sections

    # Display tasks incrementally
    start_idx = (current_page - 1) * tasks_per_page
    end_idx = min(start_idx + tasks_per_page, len(tasks))

    print("\nAll Tasks:")
    for status in ["Pending", "In Progress", "Complete", "Cancelled"]:
        print(f"\n{status} Tasks:")
        for idx, task in enumerate(tasks[start_idx:end_idx], start=start_idx+1):
            if task["status"] == status:
                total_steps = int(config[task["stage"]]["Estimated_Time_Minutes"])
                remaining_steps = total_steps - int(task["time_estimate"] // 60)
                progress = calculate_task_progress(task)
                timeline_info = f"Est. Time: {total_steps} mins | Deadline: {task['deadline']}"
                print(f"{idx}. {task['stage']}: {task['description']} ({timeline_info})")
                print(f"    Progress: {'█' * int(progress * 10)} ({progress:.0%})")
                sub_task_section = f"Sub_Tasks_{task['stage'].replace(' ', '-').replace('/', '-')}"
                if sub_task_section in config:
                    print("    Sub-tasks:")
                    for sub_task in task["sub_tasks"]:
                        sub_task_status = "Completed" if sub_task.get("completed", False) else "Pending"
                        print(f"        - {sub_task['description']} ({sub_task_status})")
    
    if show_help:
        print("\nOptions:")
        print("0. Start/Resume a task")
        print("1. Mark a task as Complete")
        print("2. Mark a task as Cancelled")
        print("3. Mark a task as Pending")
        print("4. Update estimated time for a task")
        print("5. Add a sub-task")
        print("6. Mark a sub-task as Complete")
        print("H. Hide options")  # New option to hide options
        print("Enter 'N' for next page, 'P' for previous page, or 'Q' to quit: ")
    else:
        print("Press 'H' for options")  # Prompt to show options

    current_time = time.time()
    
    # Prompt user for input to navigate pages
    print("\nPress Enter to continue or 'Q' to quit...", end="")
    while True:
        if msvcrt.kbhit():
            user_input = msvcrt.getch().decode("utf-8").upper()
            if user_input == "Q":
                #quit_pygame()

                with open("tasks.ini", "w") as config_file:
                    config.write(config_file)
                
                with open("sub_task_statuses.ini", "w") as sub_task_status_file:
                    sub_task_status_config.write(sub_task_status_file)

                exit()
            elif user_input == "\r":
                break
            elif user_input == "N":
                current_page = min(current_page + 1, (len(tasks) + tasks_per_page - 1) // tasks_per_page)
            elif user_input == "P":
                current_page = max(current_page - 1, 1)
            elif user_input == "T":
                generate_task_speech([task for task in tasks if task["status"] == "Pending"])
            elif user_input == "0":
                task_number = int(input("Enter the task number to start/resume (0 to cancel): ")) - 1

                if 0 <= task_number < len(tasks):
                    start_time = current_time
                    tasks[task_number]["status"] = "In Progress"
                    task_section = tasks[task_number]["stage"]
                    config[task_section]["Status"] = "In Progress"  # Set status to "In Progress"
                    with open("tasks.ini", "w") as config_file:
                        config.write(config_file)

                    print(f"\nTask '{tasks[task_number]['description']}' started.")
                    
                else:
                    print("Invalid task number.")
            elif user_input == "H":
                show_help = not show_help
            elif user_input == "1":
                task_number = int(input("Enter the task number to mark as complete: ")) - 1

                if 0 <= task_number < len(tasks):
                    tasks[task_number]["status"] = "Complete"
                    
                    # Earn reward points and XP
                    tasks[task_number]["reward_points"] += 1
                    tasks[task_number]["xp"] += 10
                    
                    # Level up if enough XP earned
                    if tasks[task_number]["xp"] >= tasks[task_number]["level"] * 100:
                        tasks[task_number]["xp"] = 0
                        tasks[task_number]["level"] += 1
                        print(f"Congratulations! You've reached Level {tasks[task_number]['level']}!")
                    
                    task_section = tasks[task_number]["stage"]
                    config[task_section]["Status"] = "Complete"  # Set status to "Complete"
                    with open("tasks.ini", "w") as config_file:
                        config.write(config_file)

                    print(f"\nTask '{tasks[task_number]['description']}' marked as complete.")
                    
                else:
                    print("Invalid task number.")
            elif user_input == "2":
                task_number = int(input("Enter the task number to mark as cancelled: ")) - 1

                if 0 <= task_number < len(tasks):
                    tasks[task_number]["status"] = "Cancelled"
                    task_section = tasks[task_number]["stage"]
                    config[task_section]["Status"] = "Cancelled"  # Set status to "Cancelled"
                    with open("tasks.ini", "w") as config_file:
                        config.write(config_file)

                    print(f"\nTask '{tasks[task_number]['description']}' marked as cancelled.")
                else:
                    print("Invalid task number.")
            elif user_input == "3":
                task_number = int(input("Enter the task number to mark as Pending: ")) - 1

                if 0 <= task_number < len(tasks):
                    tasks[task_number]["status"] = "Pending"
                    task_section = tasks[task_number]["stage"]
                    config[task_section]["Status"] = "Pending"
                    with open("tasks.ini", "w") as config_file:
                        config.write(config_file)

                    print(f"\nTask '{tasks[task_number]['description']}' marked as Pending.")
                else:
                    print("Invalid task number.")
            elif user_input == "4":
                task_number = int(input("Enter the task number to update estimated time: ")) - 1

                if 0 <= task_number < len(tasks):
                    new_time_estimate = int(input(f"Enter the new estimated time in minutes for '{tasks[task_number]['description']}': ")) * 60
                    tasks[task_number]["time_estimate"] = new_time_estimate

                    # Update the corresponding value in the 'tasks.ini' file
                    task_section = tasks[task_number]["stage"]
                    config[task_section]["Estimated_Time_Minutes"] = str(new_time_estimate // 60)
                    with open("tasks.ini", "w") as config_file:
                        config.write(config_file)

                    print(f"Estimated time for '{tasks[task_number]['description']}' updated to {int(new_time_estimate // 60)} mins.")
                else:
                    print("Invalid task number.")
            elif user_input == "5":
                # Display available task stages
                print("\nAvailable Task Stages:")
                for idx, task in enumerate(tasks, start=1):
                    print(f"{idx}. {task['stage']}: {task['description']}")
                
                # Prompt user to select a task stage
                selected_task_idx = int(input("Enter the index of the task stage to add a sub-task: ")) - 1
                if 0 <= selected_task_idx < len(tasks):
                    selected_task = tasks[selected_task_idx]
                    sub_task_description = input("Enter the sub-task description: ")

                    # Create the sub-task section if not present
                    sub_task_section = f"Sub_Tasks_{selected_task['stage'].replace(' ', '-').replace('/', '-')}"
                    if sub_task_section not in config:
                        config[sub_task_section] = {}
                        sub_task_status_config[sub_task_section] = {}

                    # Generate a unique sub-task key
                    sub_task_key = f"Sub_Task_{len(config[sub_task_section]) + 1}"
                    sub_task_status_key = f"Sub_Task_Status_{len(config[sub_task_section]) + 1}"

                    config[sub_task_section][sub_task_key] = sub_task_description
                    sub_task_status_config[sub_task_section][sub_task_status_key] = "Pending"  # Set initial status as Pending

                    # Save changes to 'tasks.ini'
                    with open("tasks.ini", "w") as config_file:
                        config.write(config_file)

                    # Save changes to 'sub_task_statuses.ini'
                    with open("sub_task_statuses.ini", "w") as sub_task_status_file:
                        sub_task_status_config.write(sub_task_status_file)

                    selected_task["sub_tasks"].append({"description": sub_task_description, "completed": False})
                    print("Sub-task added successfully!")
                else:
                    print("Invalid task index.")
            elif user_input == "6":
                # Display available task stages
                print("\nAvailable Task Stages:")
                for idx, task in enumerate(tasks, start=1):
                    print(f"{idx}. {task['stage']}: {task['description']}")

                # Prompt user to select a task stage
                selected_task_idx = int(input("Enter the index of the task stage for which you want to update sub-task status: ")) - 1
                if 0 <= selected_task_idx < len(tasks):
                    selected_task = tasks[selected_task_idx]
                    mark_sub_task_complete(selected_task)

                    # Save changes to 'sub_task_statuses.ini'
                    with open("sub_task_statuses.ini", "w") as sub_task_status_file:
                        sub_task_status_config.write(sub_task_status_file)
                else:
                    print("Invalid task index.")
            else:
                print("Invalid choice. Please select a valid option.")
                #time.sleep(1)
            break # Break from inner loop

print("Task Tracker closed.")