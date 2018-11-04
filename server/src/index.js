import net from 'net';
import { _connection } from './tcp';

const app = net.createServer();

const host = 'localhost';
const port = process.env.PORT || 3002;

app.listen(port, host, () => {
  console.log(`TCP Server is running on port ${port}`);
});

app.on('connection', _connection);
