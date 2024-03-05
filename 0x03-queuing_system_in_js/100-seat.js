import express from 'express';
import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';

const app = express();
const queue = kue.createQueue();
const client = redis.createClient();

async function reserveSeat(number) {
  await promisify(client.set).bind(client)('available_seats', number);
}

async function getCurrentAvailableSeats() {
  return await promisify(client.get).bind(client)('available_seats');
}
const PORT = 1245;
let reservationEnabled = true;
let availableSeats = 50;

app.get('/available_seats', async (req, res) => {
  const number = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: number });
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (job, done) => {
    const currentSeats = await getCurrentAvailableSeats();
    if (currentSeats < 1) {
      reservationEnabled = false;
      return done(new Error('Not enough seats available'));
    }
    availableSeats--;
    await reserveSeat(availableSeats);
    if (availableSeats === 0) {
      reservationEnabled = false;
    }
    done();
  });
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });

  job.on('complete', (result) => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (error) => {
    console.log(`Seat reservation job ${job.id} failed: ${error}`);
  });
});

app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
  reserveSeat(50);
});
