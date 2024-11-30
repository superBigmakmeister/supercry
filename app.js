async function hashFile(file) {
    const arrayBuffer = await file.arrayBuffer();
    const wordArray = CryptoJS.lib.WordArray.create(new Uint8Array(arrayBuffer));
    const hashHex = CryptoJS.SHA256(wordArray).toString();
    return hashHex;
}

function prettyTime(timestamp) {
    const date = new Date(timestamp * 1000);

    // Форматирование даты и времени
    const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false // 24-часовой формат
    };

    const formattedDate = date.toLocaleString('ru-RU', options);
    console.log(formattedDate); // Например: "01.10.2021, 00:00:00"
    return formattedDate;
}

async function updateFileData() {

    const input = document.getElementById("fileInput");
    const outputField = document.getElementById("outputField");
    const regButt = document.getElementById("registrateButton");
    const hiddenHashField = document.getElementById("hiddenHashField");
    const file = document.getElementById("fileInput").files[0];

    if (!file) {
        outputField.innerText = 'Файл не выбран.';
        hiddenHashField.innerText = '';
    } else {
        const hash = await hashFile(file);
        outputField.innerText = 'Хэш файла: ' + hash;
        hiddenHashField.innerText = hash;
        document.getElementById('promocode').style = 'display: block';
        regButt.disabled = false;
        const data = {
            inputhash: document.getElementById('hiddenHashField').innerText,
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
                return response.json();
            })
            .then(data => {

                document.getElementById('loadFile').style = "display: none";
                console.log(JSON.stringify(data))
                if (data['transid'] == null) {
                    document.getElementById('infostatus').innerText = "файл еще не зарегистрирован";
                    document.getElementById('infotime').innerText = "";
                    document.getElementById('infoscript').innerText = "";
                    document.getElementById('infotxid').innerText = "";
                    document.getElementById('infohelp').innerText = "если вы уже отправляли файл на регистрацию, рекомендуется подождать 20-30 минут, чтобы информация о нем появилась в блокчейне";
                    document.getElementById('loadFile').style = "display: block";
                } else {
                    document.getElementById('promocode').style = 'display: none';
                    regButt.disabled = true;
                    document.getElementById('infostatus').innerText = "файл уже зарегистрирован";
                    document.getElementById('infotime').innerText = "дата регистрации: " + prettyTime(parseInt(data['time']));
                    //document.getElementById('infoscript').innerHTML = "поле верификации: " + data["op_return"].slice(0, 4) + "<b>" + data["op_return"].slice(4) + "</b>";
                    document.getElementById('infotxid').innerHTML = "ID транзакции: " +
                        "<a href='https://blockchain.info/tx/" + data['transid'] + "'>" + data["transid"] + "</a>";
                    //+ "<a href='https://blockchain.info/rawtx/" + data['transid'] + "?format=json'>" +  data["transid"] + "</a>";
                    document.getElementById('infohelp').innerHTML = "для самостоятельной верификации нажмите на id транзакции и в нижней части информации о транзакции переключитесь на вид JSON и найдите поле script, значение которого начинается с 6a, оно должно включать в себя хэш файла и совпадать со следующей строчкой: " + data["op_return"].slice(0, 4) + "<b>" + data["op_return"].slice(4) + "</b>";
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                document.getElementById('output').innerHTML = 'Ошибка при загрузке файла';
            });
    }
}

function onload_() {
    const input = document.getElementById("fileInput");
    const outputField = document.getElementById("outputField");
    const regButt = document.getElementById("registrateButton");
    const hiddenHashField = document.getElementById("hiddenHashField");
    regButt.disabled = true;

    document.getElementById('loadFile').addEventListener('click', async () => {
        document.getElementById('infostatus').innerText = "обновляем информацию";
        document.getElementById('infohelp').innerText = "";
        updateFileData();
    });
    input.addEventListener('change', async () => {
        updateFileData();

    });

    regButt.addEventListener('click', function(event) {
        event.preventDefault();
        const data = {
            inputhash: document.getElementById('hiddenHashField').innerText,
            promocode: document.getElementById('promocode').value,
        };

        jsonData = JSON.stringify(data)
        console.log("jsonData = " + jsonData)

        fetch('hashreg', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: jsonData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Сеть ответила с ошибкой ' + response.status);
                }
                return response.text();
            })
            .then(scriptReply => {
                if (scriptReply.slice(0, 7) == 'error: ') {
                    document.getElementById('infostatus').innerHTML = '<span style="color: red">ошибка: ' + scriptReply.slice(7) + '</span>';
                } else {

                    console.log('Успех: ', scriptReply);
                    //updateFileData();
                    document.getElementById('infostatus').innerText = "файл отправлен на регистрацию";
                    document.getElementById('infohelp').innerText = "рекомендуется подождать 20-30 минут, чтобы информация о нем появилась в блокчейне";
                    document.getElementById('infotime').innerText = "";
                    document.getElementById('infoscript').innerText = "";
                    document.getElementById('infotxid').innerText = "";
                }
            })
            .catch((error) => {
                console.error('Ошибка:', error.message);
                document.getElementById('infostatus').innerHTML = '<span style="color: red"> ошибка при подключении к серверу </span>';
            });
    });
}

window.onload = onload_
