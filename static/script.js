document.addEventListener('DOMContentLoaded', () => {
    const getInfoBtn = document.getElementById('get-info-btn');
    const youtubeUrlInput = document.getElementById('youtube-url');
    const loader = document.getElementById('loader');
    const videoInfoDiv = document.getElementById('video-info');
    const videoTitle = document.getElementById('video-title');
    const videoThumbnail = document.getElementById('video-thumbnail');
    const formatsTable = document.getElementById('formats-table');

    getInfoBtn.addEventListener('click', async () => {
        const url = youtubeUrlInput.value.trim();
        if (!url) {
            alert('Please enter a YouTube URL');
            return;
        }

        loader.classList.remove('hidden');
        videoInfoDiv.classList.add('hidden');
        formatsTable.innerHTML = '';


        try {
            const response = await fetch('/get_info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url })
            });

            loader.classList.add('hidden');

            if (!response.ok) {
                const errorData = await response.json();
                alert(`Error: ${errorData.error}`);
                return;
            }

            const data = await response.json();

            videoTitle.textContent = data.title;
            videoThumbnail.src = data.thumbnail;
            videoInfoDiv.classList.remove('hidden');

            // Populate formats table
            let tableHtml = '<tr><th>Resolution</th><th>Extension</th><th>Video Codec</th><th>Audio Codec</th><th>Download</th></tr>';
            data.formats.forEach(format => {
                const downloadUrl = `/download?url=${encodeURIComponent(url)}&format_id=${format.format_id}&title=${encodeURIComponent(data.title)}&ext=${format.ext}&id=${data.id}`;
                tableHtml += `<tr>
                    <td>${format.resolution}</td>
                    <td>${format.ext}</td>
                    <td>${format.vcodec}</td>
                    <td>${format.acodec}</td>
                    <td><a href="${downloadUrl}" target="_blank">Download</a></td>
                </tr>`;
            });
            formatsTable.innerHTML = tableHtml;

        } catch (error) {
            loader.classList.add('hidden');
            alert('An error occurred. Please check the console for details.');
            console.error(error);
        }
    });
});
