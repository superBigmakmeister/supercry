

async function hashFile(file) 
{
    const arrayBuffer = await file.arrayBuffer(); 
    const wordArray = CryptoJS.lib.WordArray.create(new Uint8Array(arrayBuffer));
    const hashHex = CryptoJS.SHA256(wordArray).toString();
    return hashHex;
}


function onload_()
{
    const input = document.getElementById("fileInput");
    const outputField = document.getElementById("outputField"); 
    const inputField = document.getElementById("inputField"); 
    const regButt = document.getElementById("registrateButton");
    const hiddenHashField = document.getElementById("hiddenHashField"); 
    regButt.disabled = true; 

    input.addEventListener('change', async () => {
        const file = input.files[0];
        
        if (file)
        {
            const hash = await hashFile(file);
            outputField.innerText = 'Хэш файла: ' + hash;
            hiddenHashField.innerText = hash;
            
            regButt.disabled = false;
        } 
        else 
        {
            outputField.innerText = 'Файл не выбран.';
        }
    });
    
    regButt.addEventListener('click', function(event) {
        event.preventDefault();
        const data = {
            inputhash: document.getElementById('hiddenHashField').innerText,
            inputcomment: document.getElementById('inputField').value
        };

	jsonData = JSON.stringify(data) 
	console.log("jsonData = " + jsonData)

        fetch('hashreg', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body:jsonData 
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Сеть ответила с ошибкой ' + response.status);
            }
            return response.text();
        })
        .then(scriptReply => {
            console.log('Успех: ', scriptReply);
        })
        .catch((error) => {
            console.error('Ошибка:', error.message);
        });
    });
}

window.onload = onload_;

