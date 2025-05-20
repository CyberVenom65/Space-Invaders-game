// Space Invaders Web Version - Enhanced game.js with assets and full features

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

const WIDTH = 600;
const HEIGHT = 600;

let score = 0;
let lives = 3;
let gameRunning = false;
let currentWave = 1;
let waves = 3;
let powerUpActive = false;
let powerUpTimer = 0;
const powerUpDuration = 5000; // 5 seconds

// Player settings
const playerWidth = 50;
const playerHeight = 50;
const playerSpeed = 3;

// Bullet settings
const bulletWidth = 5;
const bulletHeight = 20;
const bulletSpeed = 10;
let bulletCooldownTimer = 0;
const bulletCooldownInterval = 300; // milliseconds

// Alien settings
const alienWidth = 50;
const alienHeight = 50;
const alienSpeed = 1.2;
let alienDirection = 1; // 1 = right, -1 = left
const alienMinY = 55; // 20 units below score text height (35) + 20
const alienMaxY = HEIGHT - 250;

// Alien bullet settings
const alienBulletWidth = 5;
const alienBulletHeight = 20;
const alienBulletSpeed = 5;
let alienBulletCooldownTimer = 0;
let alienBulletCooldownInterval = 1500;
const alienBulletMinInterval = 500;
let intervalReductionTimer = 0;
const intervalReductionInterval = 60000; // 1 minute

// Power-up settings
const powerUpWidth = 40;
const powerUpHeight = 40;
const powerUpSpeed = 3;
let powerUp = null;

// Player lives display settings
const lifeWidth = 40;
const lifeHeight = 40;

// Background scroll
let scroll = 0;
let bgHeight = 0;
let tiles = 0;

// Game objects
let player;
let bullets = [];
let aliens = [];
let alienBullets = [];
let livesDisplay = [];

// Keyboard input
const keys = {
    left: false,
    right: false,
    up: false,
    down: false,
    space: false,
};

// Load images
const assets = {};
const assetPaths = {
    player: 'assets/player.png',
    alien: 'assets/alien.png',
    alien1: 'assets/alien1.png',
    alien2: 'assets/alien2.png',
    bg: 'assets/bg.png',
    bg1: 'assets/bg1.jpg',
    life: 'assets/life.png',
    powerUp: 'assets/power_up.png',
};

function loadAssets(callback) {
    let loadedCount = 0;
    const totalAssets = Object.keys(assetPaths).length;
    for (const key in assetPaths) {
        assets[key] = new Image();
        assets[key].src = assetPaths[key];
        assets[key].onload = () => {
            loadedCount++;
            if (loadedCount === totalAssets) {
                callback();
            }
        };
        assets[key].onerror = () => {
            console.error('Failed to load asset:', assetPaths[key]);
        };
    }
}

function init() {
    player = {
        x: WIDTH / 2 - playerWidth / 2,
        y: HEIGHT - playerHeight - 10,
        width: playerWidth,
        height: playerHeight,
    };
    bullets = [];
    aliens = [];
    alienBullets = [];
    alienDirection = 1;
    score = 0;
    lives = 3;
    currentWave = 1;
    waves = Math.floor(Math.random() * 6) + 3; // 3 to 8 waves
    powerUpActive = false;
    powerUpTimer = 0;
    alienBulletCooldownInterval = 1500;
    intervalReductionTimer = 0;
    livesDisplay = [];
    for (let i = 0; i < lives; i++) {
        livesDisplay.push({
            x: WIDTH - (i + 1) * (lifeWidth + 10),
            y: 10,
            width: lifeWidth,
            height: lifeHeight,
        });
    }
    scroll = 0;
    bgHeight = assets.bg.height * (WIDTH / assets.bg.width);
    tiles = Math.ceil(HEIGHT / bgHeight) + 1;
    createAliens();
    updateScore();
    updateLives();
}

function createAliens() {
    aliens = [];
    const cols = Math.floor(WIDTH / (alienWidth + 10)) - 2;
    for (let row = 0; row < 4; row++) {
        for (let col = 1; col <= cols; col++) {
            aliens.push({
                x: col * (alienWidth + 10),
                y: row * (alienHeight + 25) + alienMinY + 10,
                width: alienWidth,
                height: alienHeight,
                hits: 0,
                type: 'alien',
            });
        }
    }
    // Replace some aliens with alien1 and alien2 based on wave count
    if (currentWave >= 3) {
        replaceAliensType('alien1', 11);
    }
    if (currentWave >= 5) {
        replaceAliensType('alien2', 11);
    }
}

function replaceAliensType(type, count) {
    const candidates = aliens.filter(a => a.type === 'alien');
    for (let i = 0; i < count && candidates.length > 0; i++) {
        const index = Math.floor(Math.random() * candidates.length);
        candidates[index].type = type;
        candidates.splice(index, 1);
    }
}

function updateScore() {
    document.getElementById('scoreboard').textContent = 'Score: ' + score;
}

function updateLives() {
    document.getElementById('lives').textContent = 'Lives: ' + lives;
}

function drawBackground() {
    for (let i = 0; i < tiles; i++) {
        ctx.drawImage(assets.bg, 0, i * bgHeight - scroll, WIDTH, bgHeight);
    }
}

function drawPlayer() {
    ctx.drawImage(assets.player, player.x, player.y, player.width, player.height);
}

function drawBullets() {
    ctx.fillStyle = 'white';
    bullets.forEach(bullet => {
        ctx.beginPath();
        ctx.moveTo(bullet.x + bullet.width / 2, bullet.y);
        ctx.lineTo(bullet.x, bullet.y + bullet.height);
        ctx.lineTo(bullet.x + bullet.width, bullet.y + bullet.height);
        ctx.closePath();
        ctx.fill();
    });
}

function drawAlienBullets() {
    ctx.fillStyle = 'red';
    alienBullets.forEach(bullet => {
        ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
    });
}

function drawAliens() {
    aliens.forEach(alien => {
        let sprite;
        if (alien.type === 'alien1') sprite = assets.alien1;
        else if (alien.type === 'alien2') sprite = assets.alien2;
        else sprite = assets.alien;
        ctx.drawImage(sprite, alien.x, alien.y, alien.width, alien.height);
    });
}

function drawLives() {
    livesDisplay.forEach(life => {
        ctx.drawImage(assets.life, life.x, life.y, life.width, life.height);
    });
}

function drawPowerUp() {
    if (powerUp) {
        ctx.drawImage(assets.powerUp, powerUp.x, powerUp.y, powerUp.width, powerUp.height);
    }
}

function movePlayer() {
    if (keys.left && player.x > 0) {
        player.x -= playerSpeed;
    }
    if (keys.right && player.x + player.width < WIDTH) {
        player.x += playerSpeed;
    }
    if (keys.up && player.y > HEIGHT - playerHeight - 200) {
        player.y -= playerSpeed;
    }
    if (keys.down && player.y + player.height < HEIGHT - 10) {
        player.y += playerSpeed;
    }
}

function moveBullets() {
    bullets.forEach((bullet, index) => {
        bullet.y -= bulletSpeed;
        if (bullet.y + bullet.height < 0) {
            bullets.splice(index, 1);
        }
    });
}

function moveAlienBullets() {
    alienBullets.forEach((bullet, index) => {
        bullet.y += alienBulletSpeed;
        if (bullet.y > HEIGHT) {
            alienBullets.splice(index, 1);
        }
    });
}

function moveAliens() {
    let hitEdge = false;
    aliens.forEach(alien => {
        alien.x += alienDirection * alienSpeed;
        if (alien.x <= 25 || alien.x + alien.width >= WIDTH - 25) {
            hitEdge = true;
        }
    });
    if (hitEdge) {
        alienDirection *= -1;
        // Removed vertical movement on edge hit to keep aliens moving only sideways
        // aliens.forEach(alien => {
        //     alien.y += alienHeight / 2;
        // });
    }
}

function checkCollisions() {
    // Player bullets vs aliens
    bullets.forEach((bullet, bIndex) => {
        aliens.forEach((alien, aIndex) => {
            if (
                bullet.x < alien.x + alien.width &&
                bullet.x + bullet.width > alien.x &&
                bullet.y < alien.y + alien.height &&
                bullet.y + bullet.height > alien.y
            ) {
                bullets.splice(bIndex, 1);
                alien.hits++;
                if (
                    (alien.type === 'alien1' && alien.hits >= 3) ||
                    (alien.type === 'alien2' && alien.hits >= 5) ||
                    (alien.type === 'alien' && alien.hits >= 1)
                ) {
                    aliens.splice(aIndex, 1);
                    if (alien.type === 'alien1') score += 3;
                    else if (alien.type === 'alien2') score += 5;
                    else score += 1;
                    updateScore();
                }
            }
        });
    });

    // Alien bullets vs player
    alienBullets.forEach((bullet, index) => {
        if (
            bullet.x < player.x + player.width &&
            bullet.x + bullet.width > player.x &&
            bullet.y < player.y + player.height &&
            bullet.y + bullet.height > player.y
        ) {
            alienBullets.splice(index, 1);
            if (lives > 0) {
                lives--;
                livesDisplay.pop();
                updateLives();
            }
            if (lives === 0) {
                gameOver();
            }
        }
    });

    // Aliens vs player
    aliens.forEach(alien => {
        if (
            alien.x < player.x + player.width &&
            alien.x + alien.width > player.x &&
            alien.y + alien.height > player.y
        ) {
            gameOver();
        }
    });

    // Player vs power-up
    if (powerUp && 
        player.x < powerUp.x + powerUp.width &&
        player.x + player.width > powerUp.x &&
        player.y < powerUp.y + powerUp.height &&
        player.y + player.height > powerUp.y) {
        powerUp = null;
        powerUpActive = true;
        powerUpTimer = Date.now();
    }
}

function spawnAlienBullet() {
    if (alienBullets.length === 0 && aliens.length > 0 && alienBulletCooldownTimer >= alienBulletCooldownInterval) {
        alienBulletCooldownTimer = 0;
        const shootingAlien = aliens[Math.floor(Math.random() * aliens.length)];
        alienBullets.push({
            x: shootingAlien.x + alienWidth / 2 - alienBulletWidth / 2,
            y: shootingAlien.y + alienHeight,
            width: alienBulletWidth,
            height: alienBulletHeight,
        });
    }
}

function spawnPowerUp() {
    if (!powerUp && Math.floor(Math.random() * 750) === 1) {
        powerUp = {
            x: Math.random() * (WIDTH - powerUpWidth),
            y: 0,
            width: powerUpWidth,
            height: powerUpHeight,
        };
    }
}

function movePowerUp() {
    if (powerUp) {
        powerUp.y += powerUpSpeed;
        if (powerUp.y > HEIGHT) {
            powerUp = null;
        }
    }
}

function updatePowerUp() {
    if (powerUpActive && Date.now() - powerUpTimer > powerUpDuration) {
        powerUpActive = false;
    }
}

function drawWaves() {
    const font = '20px Arial';
    ctx.font = font;
    ctx.fillStyle = 'white';
    const waveText = `Wave ${currentWave}`;
    const textWidth = ctx.measureText(waveText).width;
    ctx.fillText(waveText, WIDTH / 2 - textWidth / 2, 40);

    const boxWidth = 10;
    const boxHeight = 10;
    const spacing = 5;
    const totalWidth = waves * (boxWidth + spacing) - spacing;
    const startX = WIDTH / 2 - totalWidth / 2;
    const y = 45;

    for (let i = 0; i < waves; i++) {
        ctx.fillStyle = i < currentWave ? 'green' : 'gray';
        ctx.fillRect(startX + i * (boxWidth + spacing), y, boxWidth, boxHeight);
    }
}

function showStartScreen() {
    document.getElementById('startScreen').classList.remove('hidden');
    document.getElementById('gameOverScreen').classList.add('hidden');
    document.getElementById('scoreboard').textContent = 'Score: 0';
    document.getElementById('lives').textContent = 'Lives: 3';
}

function showGameOverScreen() {
    document.getElementById('gameOverScreen').classList.remove('hidden');
    document.getElementById('finalScore').textContent = `Score: ${score}`;
}

function resetGame() {
    init();
    gameRunning = true;
    document.getElementById('startScreen').classList.add('hidden');
    document.getElementById('gameOverScreen').classList.add('hidden');
    gameLoop();
}

function gameOver() {
    gameRunning = false;
    showGameOverScreen();
}

function shootBullet() {
    if (bulletCooldownTimer < bulletCooldownInterval) return;
    bulletCooldownTimer = 0;
    if (powerUpActive) {
        bullets.push({
            x: player.x + player.width / 2 - bulletWidth / 2,
            y: player.y,
            width: bulletWidth,
            height: bulletHeight,
        });
        bullets.push({
            x: player.x + player.width / 2 - bulletWidth / 2 - 10,
            y: player.y,
            width: bulletWidth,
            height: bulletHeight,
        });
        bullets.push({
            x: player.x + player.width / 2 - bulletWidth / 2 + 10,
            y: player.y,
            width: bulletWidth,
            height: bulletHeight,
        });
    } else {
        bullets.push({
            x: player.x + player.width / 2 - bulletWidth / 2,
            y: player.y,
            width: bulletWidth,
            height: bulletHeight,
        });
    }
}

function gameLoop(timestamp) {
    if (!gameRunning) return;
    ctx.clearRect(0, 0, WIDTH, HEIGHT);

    // Background scroll
    scroll += 5;
    if (scroll >= bgHeight) scroll = 0;
    drawBackground();

    movePlayer();
    moveBullets();
    moveAlienBullets();
    moveAliens();
    movePowerUp();

    checkCollisions();
    updatePowerUp();

    spawnAlienBullet();
    spawnPowerUp();

    drawPlayer();
    drawBullets();
    drawAlienBullets();
    drawAliens();
    drawLives();
    drawPowerUp();
    drawWaves();

    bulletCooldownTimer += 16.67; // Approximate frame time in ms
    alienBulletCooldownTimer += 16.67;
    intervalReductionTimer += 16.67;

    if (intervalReductionTimer >= intervalReductionInterval) {
        intervalReductionTimer = 0;
        if (alienBulletCooldownInterval > alienBulletMinInterval) {
            alienBulletCooldownInterval = Math.max(alienBulletCooldownInterval - 100, alienBulletMinInterval);
        }
    }

    // Check if all aliens are cleared
    if (aliens.length === 0) {
        currentWave++;
        if (currentWave > waves) {
            // Game won, reset waves
            waves = Math.floor(Math.random() * 6) + 3;
            currentWave = 1;
        }
        createAliens();
    }

    requestAnimationFrame(gameLoop);
}

// Event listeners
document.addEventListener('keydown', e => {
    if (e.code === 'ArrowLeft') keys.left = true;
    if (e.code === 'ArrowRight') keys.right = true;
    if (e.code === 'ArrowUp') keys.up = true;
    if (e.code === 'ArrowDown') keys.down = true;
    if (e.code === 'Space') keys.space = true;
});

document.addEventListener('keyup', e => {
    if (e.code === 'ArrowLeft') keys.left = false;
    if (e.code === 'ArrowRight') keys.right = false;
    if (e.code === 'ArrowUp') keys.up = false;
    if (e.code === 'ArrowDown') keys.down = false;
    if (e.code === 'Space') {
        keys.space = false;
        shootBullet();
    }
});

document.getElementById('playButton').addEventListener('click', () => {
    resetGame();
});

document.getElementById('restartButton').addEventListener('click', () => {
    resetGame();
});

document.getElementById('exitButton').addEventListener('click', () => {
    gameRunning = false;
    showStartScreen();
});

// Load assets and show start screen
loadAssets(() => {
    showStartScreen();
});
