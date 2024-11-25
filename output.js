function eventListenerSetUp() {
    var input = document.getElementById('loadFile')
    input.addEventListener('change', async () => {
        const file = input.files[0];

        if (!file) {
            outputField.innerText = 'Файл не выбран.';
            hiddenHashField.innerText = '';
        } else {
            const hash = await hashFile(file);
            outputField.innerText = 'Хэш файла: ' + hash;
            hiddenHashField.innerText = hash;

            regButt.disabled = false;
            const data = {
                inputhash: document.getElementById('hiddenHashField').innerText,
                inputcomment: document.getElementById('inputField').value
            };

            jsonData = JSON.stringify(data)
            console.log("jsonData = " + jsonData)
            fetch('hashcheck', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: jsonData
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Сеть не в порядке: ' + response.statusText);
                    }
                    return response.text();
                })
                .then(text => {

                    console.log(text)
                    //document.getElementById('output').innerHTML = firstTwoLines;
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    document.getElementById('output').innerHTML = 'Ошибка при загрузке файла';
                });
        }
    });
}
