import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const client = redis.createClient();
const getAsync = () => promisify(client.get).bind(client);
const setAsync = () => promisify(client.set).bind(client);

const listProducts = [
  {
    Id: 1,
    name: 'Suitcase 250',
    price: 50,
    stock: 4,
  },
  {
    Id: 2,
    name: 'Suitcase 450',
    price: 100,
    stock: 10,
  },
  {
    Id: 3,
    name: 'Suitcase 650',
    price: 350,
    stock: 2,
  },
  {
    Id: 4,
    name: 'Suitcase 1050',
    price: 550,
    stock: 5,
  },
  {
    Id: 5,
    name: 'Suitcase 1950',
    price: 550,
    stock: 0,
  },
];

function getItemById(id) {
  const item = listProducts.filter((elem) => elem.Id === id);
  return item;
}

async function reserveStockById(itemId, stock) {
    const key = `item.${itemId}`;
    await setAsync()(key, JSON.stringify(stock));
}

const getCurrentReservedStockById = async (itemId) => {
    console.log(itemId);
    const stock = await getAsync()(`item.${itemId}`);
    console.log(stock);
    return stock;

};

app.get('/list_products', (req, res) => {
  const object = listProducts.map((item) => ({
    itemId: item.Id,
    itemName: item.name,
    price: item.price,
    initialAvailableQuantity: item.stock,
  }));
  res.json(object);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = req.params.itemId;
    let stock = await getCurrentReservedStockById(itemId);
    if (stock) {
      stock = JSON.parse(stock);
      res.json({
        itemId: stock.Id,
        itemName: stock.name,
        price: stock.price,
        initialAvailableQuantity: stock.stock,
        currentQuantity: stock.stock,
      });
    } else {
      res.json({ status: 'Product not found' })
    }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = +req.params.itemId;
  let items = getItemById(itemId);
  if (items.length > 0) {
    const item = items[0];
    if (item.stock > 0) {
      reserveStockById(itemId, item);
      res.json({ status: 'Reservation confirmed', itemId });
    } else {
      res.json({ status: 'Not enough stock available', itemId });
    }
  } else {
    res.json({ status: 'Product not found' });
  }
});

app.listen('1245', () => {
  console.log('The server is listening on 1245');
});
