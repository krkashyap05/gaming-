document.addEventListener('DOMContentLoaded', () => {
    const getInfoBtn = document.getElementById('get-info-btn');
    const youtubeUrlInput = document.getElementById('youtube-url');
    const loader = document.getElementById('loader');
    const videoInfoDiv = document.getElementById('video-info');
    const videoTitle = document.getElementById('video-title');
    const videoThumbnail = document.getElementById('video-thumbnail');
    const videoFormatsTable = document.getElementById('video-formats');
    const audioFormatsTable = document.getElementById('audio-formats');

    getInfoBtn.addEventListener('click', async () => {
        const url = youtubeUrlInput.value.trim();
        if (!url) {
            alert('Please enter a YouTube URL');
            return;
        }

        loader.classList.remove('hidden');
        videoInfoDiv.classList.add('hidden');
        videoFormatsTable.innerHTML = '';
        audioFormatsTable.innerHTML = '';


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

            // Populate video formats
            let videoHtml = '<tr><th>Resolution</th><th>Extension</th><th>Video Codec</th><th>Audio Codec</th><th>Download</th></tr>';
            data.formats.forEach(format => {
                const downloadUrl = `/download?url=${encodeURIComponent(url)}&format_id=${format.format_id}&title=${encodeURIComponent(data.title)}&ext=${format.ext}`;
                videoHtml += `<tr>
                    <td>${format.resolution}</td>
                    <td>${format.ext}</td>
                    <td>${format.vcodec}</td>
                    <td>${format.acodec || 'none'}</td>
                    <td><a href="${downloadUrl}" target="_blank">Download</a></td>
                </tr>`;
            });
            videoFormatsTable.innerHTML = videoHtml;

            // Populate audio formats
            let audioHtml = '<tr><th>Bitrate</th><th>Extension</th><th>Audio Codec</th><th>Download</th></tr>';
            data.audio_formats.forEach(format => {
                const downloadUrl = `/download?url=${encodeURIComponent(url)}&format_id=${format.format_id}&title=${encodeURIComponent(data.title)}&ext=${format.ext}`;
                audioHtml += `<tr>
                    <td>${format.abr} kbps</td>
                    <td>${format.ext}</td>
                    <td>${format.acodec}</td>
                    <td><a href="${downloadUrl}" target="_blank">Download</a></td>
                </tr>`;
            });
            audioFormatsTable.innerHTML = audioHtml;


        } catch (error) {
            loader.classList.add('hidden');
            alert('An error occurred. Please check the console for details.');
            console.error(error);
        }
    });
});
