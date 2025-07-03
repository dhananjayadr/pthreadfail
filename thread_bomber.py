#!/usr/bin/python3

import threading
import time
import os
import sys
from concurrent.futures import ThreadPoolExecutor

class ThreadBomber:
    def __init__(self):
        self.success_count = 0
        self.fail_count = 0
        self.threads = []
        self.lock = threading.Lock()
        
    def worker_thread(self, thread_id):
        """Worker function that just sleeps to keep thread alive"""
        try:
            time.sleep(300)  # 5 minutes
        except KeyboardInterrupt:
            pass
    
    def monitor_progress(self):
        """Monitor thread creation progress"""
        while True:
            try:
                time.sleep(5)
                with self.lock:
                    print(f"Threads created: {len(self.threads)}, Success: {self.success_count}, Failed: {self.fail_count}")
                    
                # Print memory info
                try:
                    with open('/proc/meminfo', 'r') as f:
                        meminfo = f.read()
                        for line in meminfo.split('\n'):
                            if 'CommitLimit' in line or 'Committed_AS' in line:
                                print(f"  {line.strip()}")
                except:
                    pass
                    
            except KeyboardInterrupt:
                break
    
    def create_threads(self, max_threads=10000):
        """Create threads and monitor for failures"""
        print(f"Starting Python thread creation test...")
        print(f"Target threads: {max_threads}")
        print(f"Python version: {sys.version}")
        
        # Start monitor thread
        monitor = threading.Thread(target=self.monitor_progress, daemon=True)
        monitor.start()
        
        for i in range(max_threads):
            try:
                thread = threading.Thread(target=self.worker_thread, args=(i,))
                thread.daemon = True
                thread.start()
                
                with self.lock:
                    self.threads.append(thread)
                    self.success_count += 1
                
                # Small delay every 100 threads
                if i % 100 == 0:
                    time.sleep(0.01)
                    
            except Exception as e:
                with self.lock:
                    self.fail_count += 1
                print(f"Failed to create thread {i}: {e}")
                
                # Check if it's a resource error
                if "can't start new thread" in str(e) or "Resource temporarily unavailable" in str(e):
                    print(f"Hit thread creation limit! This could be due to:")
                    print(f"  - Virtual memory overcommit limit")
                    print(f"  - System thread limit")
                    print(f"  - Process thread limit")
                    break
        
        print(f"Thread creation completed!")
        print(f"Final count - Success: {self.success_count}, Failed: {self.fail_count}")
        
        # Keep main thread alive
        try:
            time.sleep(60)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    max_threads = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    bomber = ThreadBomber()
    bomber.create_threads(max_threads)
