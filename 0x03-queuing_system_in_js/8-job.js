function createPushNotificationsJobs(jobs, queue) {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  jobs.forEach((job) => {
    const myJob = queue.create('push_notification_code_3', job).save((err) => {
      if (err) {
        console.error(`Notification job ${myJob.id} failed: ${err}`);
      } else {
        console.log(`Notification job created: ${myJob.id}`);
      }
    });

    myJob.on('complete', () => {
      console.log(`Notification job ${myJob.id} completed`);
    });

    myJob.on('failed', (err) => {
      console.error(`Notification job ${myJob.id} failed: ${err}`);
    });

    myJob.on('progress', (progress) => {
      console.log(`Notification job ${myJob.id} ${progress}% complete`);
    });
  });
}

export default createPushNotificationsJobs;
