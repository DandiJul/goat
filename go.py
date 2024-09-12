import time
import requests
import json
from datetime import datetime, timedelta

# Membaca token dari file data.txt
def read_tokens(file_path):
    with open(file_path, 'r') as file:
        tokens = [line.strip() for line in file if line.strip()]
    return tokens

# Fungsi untuk mendapatkan data pengguna
def get_user_info(token):
    headers = {
        'authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }
    response = requests.get('https://dev-api.goatsbot.xyz/users/me', headers=headers)
    return response.json()

# Fungsi untuk mendapatkan data tugas
def get_user_missions(token):
    headers = {
        'authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }
    response = requests.get('https://api-mission.goatsbot.xyz/missions/user', headers=headers)
    return response.json()

# Fungsi untuk menyelesaikan tugas berdasarkan ID misi
def complete_task(token, task):
    headers = {
        'authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }
    url = f'https://dev-api.goatsbot.xyz/missions/action/{task["_id"]}'
    response = requests.post(url, headers=headers)
    
    if response.status_code == 201:
        print(f"Mission '{task['name']}' completed successfully.")
    else:
        print(f"Failed to complete mission '{task['name']}'. Status Code: {response.status_code}")

# Fungsi untuk menampilkan informasi akun dan tugas
def display_info(user_info, missions):
    print(f"Username: {user_info['user_name']}")
    print(f"Balance: {user_info['balance']}")
    print("Missions:")
    for project, tasks in missions.items():
        print(f"- Project: {project}")
        for task in tasks:
            print(f"  - Mission: {task['name']}")
            print(f"    Reward: {task['reward']}")
            print(f"    Status: {'Completed' if task['status'] else 'Incomplete'}")

# Fungsi utama untuk menjalankan proses
def main():
    tokens = read_tokens('data.txt')
    total_accounts = len(tokens)
    print(f"Total Accounts: {total_accounts}")

    for index, token in enumerate(tokens):
        print(f"\nProcessing Account {index + 1}/{total_accounts}")
        user_info = get_user_info(token)
        missions = get_user_missions(token)
        display_info(user_info, missions)

        # Menyelesaikan semua tugas yang belum selesai
        for project, tasks in missions.items():
            for task in tasks:
                if not task['status']:  # Jika tugas belum selesai
                    complete_task(token, task)

        if index < total_accounts - 1:
            print("Waiting for 5 seconds before switching to the next account...")
            time.sleep(5)

    print("\nAll accounts processed. Starting 1-day countdown...")

    end_time = datetime.now() + timedelta(days=1)
    while datetime.now() < end_time:
        remaining_time = end_time - datetime.now()
        print(f"Time remaining: {str(remaining_time).split('.')[0]}", end='\r')
        time.sleep(1)
    
    print("\n1-day countdown finished. Restarting process...\n")
    main()

# Memulai proses
main()
