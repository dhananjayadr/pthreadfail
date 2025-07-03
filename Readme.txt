LINUX VIRTUAL MEMORY OVERCOMMIT THREAD CREATION TEST SUITE
===========================================================

OBJECTIVE
=========
Test scripts to validate and reproduce the virtual memory overcommit behavior 
that causes thread creation failures using C, Java, and Python, as diagnosed 
in the blog post:
https://dhananjayadr.vercel.app/posts/data/linux-virtual-memory-overcommit-blocked-java-native-thread-creation

TEST FILES
==========
File                         | Purpose
---------------------------- | ----------------------------------------------------------
monitor_system.sh            | Display current system memory and overcommit settings
thread_bomber.c              | C program using direct pthread_create() calls
thread_bomber.py             | Python program using threading.Thread
ThreadBomber.java            | Java program to create threads and trigger the issue
thread_bomber_futures.py     | Python program using ThreadPoolExecutor
run_test.sh                  | Complete test suite that demonstrates the issue and fixes

PREREQUISITES
=============
Required packages:
- openjdk-11-jdk (or openjdk-17-jdk)
- gcc
- python3

Required permissions:
- sudo access to modify kernel parameters (vm.overcommit_memory, vm.overcommit_ratio)

SETUP
=====
1. Clone repository and give execute permission for the scripts
   chmod +x *.sh *.py

RUNNING THE TESTS
=================

1. Check current system state
-----------------------------
./monitor

2. Run individual tests
-----------------------
C test:
gcc -pthread -o thread_bomber thread_bomber.c
./thread_bomber 5000

Python tests:
python3 thread_bomber.py 3000
python3 thread_bomber_futures.py 2000

Java test:
javac ThreadBomber.java
java ThreadBomber 3000

3. Run complete test suite
--------------------------
sudo ./test

TEST SCENARIOS
==============

1. Reproduce EAGAIN Error
-------------------------
Demonstrate the original problem with restrictive overcommit settings:

sudo sysctl vm.overcommit_memory=2
sudo sysctl vm.overcommit_ratio=10
./monitor

# Run test - should fail with EAGAIN while RAM is available
./thread_bomber 5000

Expected Result: Thread creation fails with EAGAIN error even though 
physical RAM is available.

2. Validate the Fix
-------------------
Increase overcommit ratio to allow more virtual memory:

sudo sysctl vm.overcommit_ratio=75
./monitor

# Run same test - should create more threads successfully
./thread_bomber 5000

Expected Result: More threads created successfully with the same 
physical memory usage.

3. No Virtual Memory Limits
---------------------------
Remove virtual memory accounting restrictions:

sudo sysctl vm.overcommit_memory=1
./monitor

# Test is now limited by actual system resources, not virtual memory accounting
./thread_bomber 8000

Expected Result: Thread creation only limited by actual system resources 
(RAM, process limits, etc.).
