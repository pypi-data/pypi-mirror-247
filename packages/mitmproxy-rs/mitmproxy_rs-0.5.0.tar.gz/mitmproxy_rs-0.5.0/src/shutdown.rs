use std::sync::Arc;

use anyhow::Result;
use tokio::{
    sync::{broadcast::Sender as BroadcastSender, RwLock},
    task::JoinHandle,
};

pub struct ShutdownTask {
    py_handle: JoinHandle<Result<()>>,
    wg_handle: JoinHandle<Result<()>>,
    sd_trigger: BroadcastSender<()>,
    sd_barrier: BroadcastSender<()>,
}

impl ShutdownTask {
    pub fn new(
        py_handle: JoinHandle<Result<()>>,
        wg_handle: JoinHandle<Result<()>>,
        sd_trigger: BroadcastSender<()>,
        sd_barrier: BroadcastSender<()>,
    ) -> Self {
        ShutdownTask {
            py_handle,
            wg_handle,
            sd_trigger,
            sd_barrier,
        }
    }

    pub async fn run(self) {
        let mut sd_watcher = self.sd_trigger.subscribe();
        let shutting_down = Arc::new(RwLock::new(false));

        // wait for Python interop task to return
        let py_sd_trigger = self.sd_trigger.clone();
        let py_shutting_down = shutting_down.clone();
        let py_task_handle = tokio::spawn(async move {
            match self.py_handle.await {
                Ok(Ok(())) => (),
                Ok(Err(error)) => log::error!("Python interop task failed: {}", error),
                Err(error) => log::error!("Python interop task panicked: {}", error),
            }

            if !*py_shutting_down.read().await {
                log::error!("Python interop task shut down early, exiting.");
                let _ = py_sd_trigger.send(());
            }
        });

        // wait for WireGuard server task to return
        let wg_sd_trigger = self.sd_trigger.clone();
        let wg_shutting_down = shutting_down.clone();
        let wg_task_handle = tokio::spawn(async move {
            match self.wg_handle.await {
                Ok(Ok(())) => (),
                Ok(Err(error)) => log::error!("Proxy server task failed: {}", error),
                Err(error) => log::error!("Proxy server task panicked: {}", error),
            }

            if !*wg_shutting_down.read().await {
                log::error!("Proxy server task shut down early, exiting.");
                let _ = wg_sd_trigger.send(());
            }
        });

        // wait for shutdown trigger:
        // - either `Server.stop` was called, or
        // - one of the subtasks failed early
        let _ = sd_watcher.recv().await;
        *shutting_down.write().await = true;

        // wait for all tasks to terminate and log any errors
        if let Err(error) = py_task_handle.await {
            log::error!("Shutdown of Python interop task failed: {}", error);
        }
        if let Err(error) = wg_task_handle.await {
            log::error!("Shutdown of WireGuard server task failed: {}", error);
        }

        // make `Server.wait_closed` method yield
        self.sd_barrier.send(()).ok();
    }
}
