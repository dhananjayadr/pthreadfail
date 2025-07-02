OBJECTIVE
=========
Test scripts to validate and reproduce the virtual memory overcommit behavior 
that causes Java thread creation failures, as diagnosed in the blog post:
https://dhananjayadr.vercel.app/posts/data/linux-virtual-memory-overcommit-blocked-java-native-thread-creation


TEST FILES
==========
files                        | purpose
---------------------------- | ----------------------------------------------------------
monitor                      | Display current system memory and overcommit settings
ThreadBomber.java            | Java program to create threads and trigger the issue
thread_bomber.c              | C program using direct pthread_create() calls
test                         | Complete test suite that demonstrates the issue and fixes


PREREQUISITES
=============
openjdk-11-jdk, gcc


RUNNING THE TESTS
=================
1. Run individual tests
-----------------------

Check current system state:
    ./monitor_system.sh

Compile and run C test:
    gcc -pthread -o thread_bomber thread_bomber.c
    ./thread_bomber 5000

Compile and run Java test:
    javac ThreadBomber.java
    java ThreadBomber 3000

2. Run complete test suite
--------------------------

    sudo ./test


TEST SCENARIOS
==============
1. Reproduce EAGAIN Error
-------------------------

    sudo sysctl vm.overcommit_memory=2
    sudo sysctl vm.overcommit_ratio=10
    # Run test - should fail with EAGAIN while RAM is available
    ./thread_bomber 5000

2. Validate the fix you want to check
-------------------------------------

    sudo sysctl vm.overcommit_ratio=75
    # Run same test - should create more threads successfully
    ./thread_bomber 5000

3. No Limits
------------

    sudo sysctl vm.overcommit_memory=1

Test is now limited by actual system resources, not virtual memory accounting:
    ./thread_bomber 8000
