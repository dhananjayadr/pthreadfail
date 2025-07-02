#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

void* worker_thread(void* arg) {
    sleep(300);
    return NULL;
}

int main(int argc, char* argv[]) {
    int max_threads = (argc > 1) ? atoi(argv[1]) : 10000;
    pthread_t* threads = malloc(max_threads * sizeof(pthread_t));
    int success_count = 0;
    int fail_count = 0;
    
    printf("Starting C pthread creation test...\n");
    printf("Target threads: %d\n", max_threads);
    
    for (int i = 0; i < max_threads; i++) {
        int result = pthread_create(&threads[i], NULL, worker_thread, NULL);
        
        if (result == 0) {
            success_count++;
            pthread_detach(threads[i]);
        } else {
            fail_count++;
            printf("Failed to create thread %d: %s (errno: %d)\n", 
                   i, strerror(result), result);
            
            if (result == EAGAIN) {
                printf("EAGAIN error - likely hit virtual memory overcommit limit!\n");
                break;
            }
        }
        
        if (i % 1000 == 0) {
            printf("Progress: %d threads created, %d failed\n", success_count, fail_count);
        }
        
        if (i % 100 == 0) {
            usleep(1000); // 1ms
        }
    }
    
    printf("Thread creation completed!\n");
    printf("Final count - Success: %d, Failed: %d\n", success_count, fail_count);
    
    sleep(60);
    
    free(threads);
    return 0;
}
