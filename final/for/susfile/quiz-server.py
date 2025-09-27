#!/usr/bin/env python3
import socket
import threading
import sys

# Quiz questions and answers
QUESTIONS = [
    {
        "question": "What is the actual file extension of file1.sus? (Example: .exe)",
        "answer": ".xlsm"
    },
    {
        "question": "List all child processes spawned by cmd.exe when file1.sus is executed. List them alphabetically. (Example: calc.exe, notepad.exe)",
        "answer": "certutil.exe, conhost.exe"
    },
    {
        "question": "Which malware family does file1.sus belong to? (Example: Lumma)",
        "answer": "Agent Tesla"
    },
    {
        "question": "Who is the author of file1.sus, and when was it created? (Example: Admin, 2025-01-10 13:57:52Z)",
        "answer": "Dell, 2021:08:19 14:03:52Z"
    },
    {
        "question": "How many IO Blocks inside this file? (Example: 1200",
        "answer": "512"
    },
    {
        "question": "How many macro streams were identified in file1.sus? List the streams that contain macros. (Example: 7; a,b,c,d,e,f,g)",
        "answer": "3; A3,A4,A5"
    },
    {
        "question": "Provide the VB_Name attribute for each macro stream, listed alphabetically. (Example: First_Sheet, Second_Sheet)",
        "answer": "Sheet1, ThisWorkbook, Workbook"
    },
    {
        "question": "There was likely an attempt to download a file from a suspicious IP. What is the IP address, and where is it hosted? (Example: 32.129.20.15, Japan)",
        "answer": "52.59.234.180, Germany"
    },
    {
        "question": "Which tool downloads the payload, what filename is it saved as, and what concealment technique is used? (give the VBA constant if applicable) (Example: notepad.exe, malicious.exe, vbMinimizedNoFocus)",
        "answer": "certutil.exe, Grfciafhjqghqqtyyb.exe.exe, vbHide"
    }
]

FLAG = "hacktoday{doc_d0c_dOc_maldocdocdoc}"

def display_all_questions():
    """Generate string with all questions displayed"""
    questions_text = "\n=== ALL QUESTIONS ===\n\n"
    for i, qa in enumerate(QUESTIONS, 1):
        questions_text += f"{i}. {qa['question']}\n\n"
    return questions_text

def display_status(answered_correctly, answered_incorrectly):
    """Display current status of answered questions"""
    status_text = "\n=== STATUS ===\n"
    for i in range(len(QUESTIONS)):
        if i in answered_correctly:
            status_text += f"Question {i+1}: ✓ CORRECT\n"
        elif i in answered_incorrectly:
            status_text += f"Question {i+1}: ✗ INCORRECT\n"
        else:
            status_text += f"Question {i+1}: ○ PENDING\n"
    
    total_answered = len(answered_correctly) + len(answered_incorrectly)
    status_text += f"\nProgress: {total_answered}/{len(QUESTIONS)} answered ({len(answered_correctly)} correct, {len(answered_incorrectly)} incorrect)\n"
    return status_text

def handle_client(client_socket, client_address):
    """Handle individual client connections"""
    print(f"[+] Connection from {client_address}")
    
    try:
        # Send welcome message and all questions
        welcome_msg = """
=================================================
    MALDOC EZPZ QUIZ
=================================================
Welcome, fellow cysec enjoyer!
You need to answer all 9 questions correctly to get the flag.
You can answer questions in any order by selecting the question number.
Have fun!

📥 DOWNLOAD THE SAMPLE FILE:
https://mega.nz/file/T4IlXTAJ#bB-PwOldQK4jJ3KtBPhDzK7gEAkD5imHBGv49tmowWQ

⚠️  WARNING: This file contains malware! Only analyze in a safe environment.
    Use a virtual machine or isolated sandbox for analysis.

=================================================
"""
        client_socket.send(welcome_msg.encode())
        client_socket.send(display_all_questions().encode())
        
        answered_correctly = set()
        answered_incorrectly = set()
        
        while len(answered_correctly) + len(answered_incorrectly) < len(QUESTIONS):
            # Display current status
            client_socket.send(display_status(answered_correctly, answered_incorrectly).encode())
            
            # Ask for question number
            prompt_msg = "\nWhich question would you like to answer? (Enter question number 1-9): "
            client_socket.send(prompt_msg.encode())
            
            # Receive question number
            try:
                client_socket.settimeout(120)  # 2 minute timeout
                question_num_input = client_socket.recv(1024).decode().strip()
                if not question_num_input:  # Client disconnected
                    print(f"[-] Client {client_address} disconnected")
                    return
            except socket.timeout:
                client_socket.send(b"\n[!] Timeout! Connection closed.\n")
                return
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                print(f"[-] Client {client_address} disconnected unexpectedly")
                return
            
            # Validate question number
            try:
                question_num = int(question_num_input)
                if question_num < 1 or question_num > len(QUESTIONS):
                    client_socket.send(b"[!] Invalid question number. Please enter a number between 1-9.\n")
                    continue
            except ValueError:
                client_socket.send(b"[!] Please enter a valid number.\n")
                continue
            
            question_index = question_num - 1
            
            # Check if already answered
            if question_index in answered_correctly or question_index in answered_incorrectly:
                status = "correctly" if question_index in answered_correctly else "incorrectly"
                client_socket.send(f"[!] You've already answered question {question_num} {status}. Choose another question.\n".encode())
                continue
            
            # Ask for the answer
            answer_prompt = f"\nQuestion {question_num}: {QUESTIONS[question_index]['question']}\nYour answer: "
            client_socket.send(answer_prompt.encode())
            
            # Receive answer
            try:
                answer = client_socket.recv(1024).decode().strip()
                if not answer:  # Client disconnected
                    print(f"[-] Client {client_address} disconnected")
                    return
            except socket.timeout:
                client_socket.send(b"\n[!] Timeout! Connection closed.\n")
                return
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                print(f"[-] Client {client_address} disconnected unexpectedly")
                return
            
            print(f"[?] Q{question_num} - Client {client_address} answered: '{answer}'")
            
            # Check answer (case-insensitive comparison)
            correct_answer = QUESTIONS[question_index]['answer']
            if answer.lower().strip() == correct_answer.lower().strip():
                answered_correctly.add(question_index)
                client_socket.send(f"[+] Correct! Question {question_num} marked as completed.\n".encode())
                print(f"[+] Client {client_address} answered Q{question_num} correctly")
            else:
                # Wrong answer - mark as incorrect but continue
                answered_incorrectly.add(question_index)
                client_socket.send(f"[!] Incorrect answer for Question {question_num}.\n".encode())
                print(f"[-] Client {client_address} answered Q{question_num} incorrectly")
        
        # All questions answered - check if all are correct
        if len(answered_correctly) == len(QUESTIONS):
            # All answers correct - send flag
            success_msg = f"""
=================================================
🎉 CONGRATULATIONS! 🎉
=================================================
You have successfully answered all 9 questions correctly!

Here's your flag: {FLAG}
=================================================
"""
            client_socket.send(success_msg.encode())
            print(f"[+] Client {client_address} completed the entire challenge successfully!")
        else:
            # Some answers were wrong
            failure_msg = f"""
=================================================
❌ CHALLENGE FAILED ❌
=================================================
You are not smart enough, try again.

You answered {len(answered_correctly)} out of {len(QUESTIONS)} questions correctly.
You got {len(answered_incorrectly)} questions wrong.

Please reconnect and try again!
=================================================
"""
            client_socket.send(failure_msg.encode())
            print(f"[-] Client {client_address} failed the challenge - {len(answered_correctly)}/{len(QUESTIONS)} correct")
                
    except Exception as e:
        print(f"[!] Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"[-] Connection from {client_address} closed")

def start_server(host='0.0.0.0', port=14045):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        print(f"[+] Quiz server listening on {host}:{port}")
        print(f"[+] Contestants can connect with: nc {host} {port}")
        print("[+] Press Ctrl+C to stop the server")
        
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                # Handle each client in a separate thread
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()
                
            except KeyboardInterrupt:
                print("\n[!] Server shutting down...")
                break
                
    except Exception as e:
        print(f"[!] Server error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    # Parse command line arguments
    host = '0.0.0.0'
    port = 14045
    
    if len(sys.argv) >= 2:
        port = int(sys.argv[1])
    if len(sys.argv) >= 3:
        host = sys.argv[2]
    
    start_server(host, port)
