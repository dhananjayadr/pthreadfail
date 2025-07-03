#!/usr/bin/python3

import concurrent.futures
import threading
import time
import sys
import os

def worker_task(task_id):
    """Worker function that sleeps to keep thread alive"""
    try:
        time.sleep(300)  # 5 minutes
        return f"Task {task_id} completed"
    except KeyboardInterrupt:
        return f"Task {task_id} interrupted"

def test_with_threadpool():
    """Test thread creation using ThreadPoolExecutor"""
    max_threads = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    
    print(f"Starting Python ThreadPoolExecutor test...")
    print(f"Target threads: {max_threads}")
    
    success_count = 0
    fail_count = 0
    
    try:
        # Try to create a thread pool with many threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = []
            
            for i in range(max_threads):
                try:
                    future = executor.submit(worker_task, i)
                    futures.append(future)
                    success_count += 1
                    
                    if i % 100 == 0:
                        print(f"Submitted {i} tasks")
                        # Check memory state
                        try:
                            with open('/proc/meminfo', 'r') as f:
                                for line in f:
                                    if 'CommitLimit' in line or 'Committed_AS' in line:
                                        print(f"  {line.strip()}")
                        except:
                            pass
                            
                except Exception as e:
                    fail_count += 1
                    print(f"Failed to submit task {i}: {e}")
                    break
            
            print(f"All tasks submitted. Success: {success_count}, Failed: {fail_count}")
            
            # Wait a bit to see the effect
            time.sleep(30)
            
    except Exception as e:
        print(f"ThreadPoolExecutor creation failed: {e}")
        if "can't start new thread" in str(e):
            print("Hit system thread limit!")

if __name__ == "__main__":
    test_with_threadpool()
