document.addEventListener("DOMContentLoaded", function() {
    const starCount = 30;  // Number of stars to show
    const starsContainer = document.querySelector('.stars-container');

    // Create the stars dynamically
    for (let i = 0; i < starCount; i++) {
        let star = document.createElement('div');
        star.classList.add('star');

        // Randomize the position and duration of each star
        const randomLeft = Math.random() * 100;  // Random left between 0% and 100%
        const randomTop = Math.random() * 100;  // Random top between 0% and 100%
        const randomDuration = (Math.random() * 3 + 1) + "s";  // Random duration between 1s and 4s
        const randomXMovement = Math.random() * 500 + 200; // Horizontal movement
        const randomYMovement = Math.random() * 500 + 200; // Vertical movement

        // Apply the random values to the star
        star.style.left = `${randomLeft}%`;
        star.style.top = `${randomTop}%`;
        star.style.setProperty('--duration', randomDuration);
        star.style.setProperty('--random-x', `${randomXMovement}px`);
        star.style.setProperty('--random-y', `${randomYMovement}px`);

        starsContainer.appendChild(star);
    }
});
document.addEventListener("DOMContentLoaded", function() {
    // Trigger the fade-up animation
    const animatedElements = document.querySelectorAll('.animated');
    animatedElements.forEach((el, index) => {
        // Add the fade-up class and delay based on the index
        el.classList.add('fade-up');
        el.classList.add(`delay-${index + 1}`);
    });
});
