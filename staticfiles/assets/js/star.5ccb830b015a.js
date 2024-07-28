document.addEventListener("DOMContentLoaded", function () {
    const starBackground = document.querySelector('.star-background');
    const numStars = 100;

    for (let i = 0; i < numStars; i++) {
        let star = document.createElement('div');
        star.className = 'star';
        star.style.top = Math.random() * 100 + 'vh';
        star.style.left = Math.random() * 100 + 'vw';
        star.style.animationDelay = Math.random() * 2 + 's';
        starBackground.appendChild(star);
    }
});
