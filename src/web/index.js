const socket = new WebSocket('ws://localhost:8765');

socket.addEventListener('open', (event) => {
    socket.send(0);
});

// Listen for messages
socket.addEventListener('message', (event) => {
    const coords = event.data.split(',')
    draw(parseInt(coords[0]), parseInt(coords[1]));
});

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
ctx.fillStyle = 'red';

canvas.addEventListener('click', (event) => {
    const rect = canvas.getBoundingClientRect();
    const x = event.x - rect.left;
    const y = event.y - rect.top;

    draw(x, y);
    socket.send(`${x},${y}`)
});

const draw = (x, y) => {
    ctx.beginPath();
    ctx.arc(x, y, 15, 0, Math.PI * 2, true);
    ctx.fill();
}
