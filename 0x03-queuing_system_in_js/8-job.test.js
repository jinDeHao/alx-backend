import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job';

describe('createPushNotificationsJobs', () => {
  it('display a error message if jobs is not an array', () => {
    const queue = kue.createQueue();
    kue.Job.rangeByState('inactive', 0, -1, 'asc', (err, jobs) => {
      jobs.forEach((job) => {
        job.remove();
      });
    });
    expect(() => createPushNotificationsJobs({}, queue)).to.throw(
      'Jobs is not an array'
    );
    queue.shutdown();
  });
});
