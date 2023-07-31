// replays.js
document.addEventListener('DOMContentLoaded', () => {
    // Make a GET request to the API endpoint
    fetch('/API/replays/')  // Update the URL to match your actual API endpoint URL
        .then(response => response.json())
        .then(data => {

            // Process the data and create cards for each replay
            const replaysList = document.getElementById('replays-list');
            data.forEach(replay => {
                const card = document.createElement('div');
                card.classList.add('replay-card');

                const title = document.createElement('p');
                title.textContent = `Title: ${replay.title}`;
                card.appendChild(title);

                const video = document.createElement('video');
                video.src = replay.video; // Assuming the video URL is provided in the replay data
                video.controls = true;
                card.appendChild(video);

                const game = document.createElement('p');
                game.textContent = `Game: ${replay.game}`;
                card.appendChild(game);

                const author = document.createElement('p');
                author.textContent = `Author: ${replay.author}`;
                card.appendChild(author);

                const description = document.createElement('p');
                description.textContent = `Description: ${replay.description}`;
                card.appendChild(description);

                replaysList.appendChild(card);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});


