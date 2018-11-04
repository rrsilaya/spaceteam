import uuid from 'shortid';

let sockets = [];

export const broadcast = data => {
  sockets.forEach(socket => socket.write(data));
}

export const _connection = socket => {
  socket._id = uuid.generate();
  sockets.push(socket);

  console.log(`[CONNECTED] ${socket._id}: ${socket.remoteAddress}`);

  socket.on('data', _receive(socket));
  socket.on('close', _close(socket));
}

export const _receive = socket => data => {
  console.log(`[RECEIVED] ${socket._id}: ${data}`);
  broadcast(`${socket._id}:${socket.remoteAddress} said ${data}`);
}

export const _close = socket => () => {
  console.log(`[CLOSED] ${socket._id}: ${socket.remoteAddress} `);
  sockets = sockets.filter(({ _id }) => socket._id !== _id);
}
