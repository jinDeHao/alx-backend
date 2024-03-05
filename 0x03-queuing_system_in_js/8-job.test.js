import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job';

describe('createPushNotificationsJobs', () => {
  before(() => queue.testMode.enter());
  afterEach(() => {
    queue.testMode.clear();
  });
  after(() => {
    queue.testMode.exit();
  });
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
  it('Testing the log', () => {
    const consoleLog = sinon.spy(console, 'log');
    const job = [
      {
        phoneNumber: '569865867',
        message: 'The verification code is 9627',
      },
    ];
    createPushNotificationsJobs(job, queue);

    expect(consoleLog.args[0][0]).to.includes('Notification job created:');
  });
  it('Testing the type of jobs', () => {
    const createSpy = sinon.spy(queue, 'create');
    sinonList.push(createSpy);
    const jobs = [
      {
        phoneNumber: '569865867',
        message: 'The verification code is 9657',
      },
      {
        phoneNumber: '569865867',
        message: 'The verification code is 9627',
      },
    ];
    createPushNotificationsJobs(jobs, queue);
    jobs.forEach((job) => {
      expect(createSpy.calledWith('push_notification_code_3', job)).to.be.true;
    });
  });
});
