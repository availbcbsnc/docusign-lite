const canvas = document.getElementById('signaturePad');
const ctx = canvas.getContext('2d');
let drawing = false;

function startDraw(e) {
    drawing = true;
    ctx.beginPath();
    ctx.moveTo(getX(e), getY(e));
}

function draw(e) {
    if (!drawing) return;
    ctx.lineTo(getX(e), getY(e));
    ctx.stroke();
}

function endDraw() {
    drawing = false;
}

function getX(e) {
    return e.touches ? e.touches[0].clientX - canvas.getBoundingClientRect().left : e.offsetX;
}

function getY(e) {
    return e.touches ? e.touches[0].clientY - canvas.getBoundingClientRect().top : e.offsetY;
}

canvas.addEventListener('mousedown', startDraw);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', endDraw);
canvas.addEventListener('mouseout', endDraw);

canvas.addEventListener('touchstart', startDraw);
canvas.addEventListener('touchmove', draw);
canvas.addEventListener('touchend', endDraw);

function clearSignature() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

document.getElementById('signForm').addEventListener('submit', function(e) {
    const dataURL = canvas.toDataURL('image/png');
    document.getElementById('signatureInput').value = dataURL;
});
