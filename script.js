document.addEventListener('DOMContentLoaded', () => {
    const gameContainer = document.getElementById('game-container');
    const hero = document.getElementById('hero');
    const scoreDisplay = document.getElementById('score');

    let score = 0;
    // Start hero in the center of the game container
    let heroX = (gameContainer.clientWidth - hero.clientWidth) / 2;
    let heroY = (gameContainer.clientHeight - hero.clientHeight) / 2;
    const heroSpeed = 10;

    const keys = {
        ArrowUp: false,
        ArrowDown: false,
        ArrowLeft: false,
        ArrowRight: false
    };

    // Set initial hero position
    hero.style.left = `${heroX}px`;
    hero.style.top = `${heroY}px`;

    // Handle keyboard input to track which keys are pressed
    document.addEventListener('keydown', (e) => {
        if (e.key in keys) {
            keys[e.key] = true;
        }
    });

    document.addEventListener('keyup', (e) => {
        if (e.key in keys) {
            keys[e.key] = false;
        }
    });

    function gameLoop() {
        // Update hero position based on pressed keys
        if (keys.ArrowUp && heroY > 0) {
            heroY -= heroSpeed;
        }
        if (keys.ArrowDown && heroY < gameContainer.clientHeight - hero.clientHeight) {
            heroY += heroSpeed;
        }
        if (keys.ArrowLeft && heroX > 0) {
            heroX -= heroSpeed;
        }
        if (keys.ArrowRight && heroX < gameContainer.clientWidth - hero.clientWidth) {
            heroX += heroSpeed;
        }

        hero.style.top = `${heroY}px`;
        hero.style.left = `${heroX}px`;

        // Check for collisions with trash items
        document.querySelectorAll('.trash').forEach(trash => {
            if (isColliding(hero, trash)) {
                trash.remove();
                score++;
                scoreDisplay.textContent = `Score: ${score}`;
                // Spawn a new piece of trash to replace the collected one
                spawnTrash();
            }
        });

        // Continue the game loop
        requestAnimationFrame(gameLoop);
    }

    function spawnTrash() {
        const trash = document.createElement('div');
        trash.classList.add('trash');

        // Place trash randomly within the game container
        const trashX = Math.random() * (gameContainer.clientWidth - 30);
        const trashY = Math.random() * (gameContainer.clientHeight - 30);

        trash.style.left = `${trashX}px`;
        trash.style.top = `${trashY}px`;

        gameContainer.appendChild(trash);
    }

    function isColliding(div1, div2) {
        const rect1 = div1.getBoundingClientRect();
        const rect2 = div2.getBoundingClientRect();

        return !(
            rect1.right < rect2.left ||
            rect1.left > rect2.right ||
            rect1.bottom < rect2.top ||
            rect1.top > rect2.bottom
        );
    }

    // Spawn the initial set of trash
    for (let i = 0; i < 10; i++) {
        spawnTrash();
    }

    // Start the game
    gameLoop();
});
