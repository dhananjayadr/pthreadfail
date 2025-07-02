import java.util.concurrent.atomic.AtomicInteger;

public class ThreadBomber {
    private static final AtomicInteger threadCount = new AtomicInteger(0);
    private static final AtomicInteger successCount = new AtomicInteger(0);
    private static final AtomicInteger failCount = new AtomicInteger(0);
    
    public static void main(String[] args) {
        int maxThreads = args.length > 0 ? Integer.parseInt(args[0]) : 10000;
        
        System.out.println("Starting thread creation test...");
        System.out.println("Target threads: " + maxThreads);
        
        Thread monitor = new Thread(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                try {
                    Thread.sleep(5000);
                    System.out.printf("Threads created: %d, Success: %d, Failed: %d%n", 
                        threadCount.get(), successCount.get(), failCount.get());
                    
                    Runtime runtime = Runtime.getRuntime();
                    System.out.printf("JVM Memory - Total: %d MB, Used: %d MB, Free: %d MB%n",
                        runtime.totalMemory() / 1024 / 1024,
                        (runtime.totalMemory() - runtime.freeMemory()) / 1024 / 1024,
                        runtime.freeMemory() / 1024 / 1024);
                } catch (InterruptedException e) {
                    break;
                }
            }
        });
        monitor.setDaemon(true);
        monitor.start();
        
        for (int i = 0; i < maxThreads; i++) {
            try {
                Thread worker = new Thread(() -> {
                    try {
                        Thread.sleep(300000);
                    } catch (InterruptedException e) {
                    }
                });
                
                worker.start();
                threadCount.incrementAndGet();
                successCount.incrementAndGet();
                
                if (i % 100 == 0) {
                    Thread.sleep(10);
                }
                
            } catch (OutOfMemoryError e) {
                failCount.incrementAndGet();
                System.err.println("Failed to create thread " + i + ": " + e.getMessage());
                break;
            } catch (Exception e) {
                failCount.incrementAndGet();
                System.err.println("Failed to create thread " + i + ": " + e.getMessage());
                break;
            }
        }
        
        System.out.println("Thread creation completed!");
        System.out.printf("Final count - Success: %d, Failed: %d%n", 
            successCount.get(), failCount.get());
        
        try {
            Thread.sleep(60000);
        } catch (InterruptedException e) {
        }
    }
}
