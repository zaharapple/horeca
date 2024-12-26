document.addEventListener('DOMContentLoaded', function () {
    const previews = document.querySelectorAll('.image-preview');
    previews.forEach(preview => {
        preview.addEventListener('click', () => {
            const overlay = document.createElement('div');
            overlay.style.position = 'fixed';
            overlay.style.top = '0';
            overlay.style.left = '0';
            overlay.style.width = '100%';
            overlay.style.height = '100%';
            overlay.style.background = 'rgba(0, 0, 0, 0.5)';
            overlay.style.zIndex = '9998';

            const popup = document.createElement('div');
            popup.style.position = 'fixed';
            popup.style.top = '50%';
            popup.style.left = '50%';
            popup.style.transform = 'translate(-50%, -50%)';
            popup.style.zIndex = '9999';
            popup.style.border = '1px solid #aaa';
            popup.style.background = '#fff';
            popup.style.padding = '10px';
            popup.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
            popup.style.textAlign = 'center';

            const closeBtn = document.createElement('span');
            closeBtn.innerHTML = '&times;';
            closeBtn.style.position = 'absolute';
            closeBtn.style.top = '5px';
            closeBtn.style.right = '10px';
            closeBtn.style.fontSize = '20px';
            closeBtn.style.cursor = 'pointer';
            closeBtn.style.color = '#333';

            closeBtn.addEventListener('click', () => {
                document.body.removeChild(popup);
                document.body.removeChild(overlay);
            });

            const img = document.createElement('img');
            img.src = preview.src;
            img.style.maxWidth = '90vw';
            img.style.maxHeight = '90vh';
            img.style.borderRadius = '4px';

            popup.appendChild(closeBtn);
            popup.appendChild(img);
            document.body.appendChild(overlay);
            document.body.appendChild(popup);

            overlay.addEventListener('click', () => {
                document.body.removeChild(popup);
                document.body.removeChild(overlay);
            });
        });
    });
});
