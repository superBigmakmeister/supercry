function eventListenerSetUp()
{
	document.getElementById('loadFile').addEventListener('click', function() {
	    fetch('info.txt') // Укажите путь к вашему файлу на сервере
		.then(response => {
		    if (!response.ok) {
			throw new Error('Сеть не в порядке: ' + response.statusText);
		    }
		    return response.text(); // Чтение содержимого файла как текст
		})
		.then(text => {
		    const lines = text.split('\n'); // Разделяем текст на строки
		    const firstTwoLines = lines.slice(0, 2).join('<br>'); // Берем первые две строки и объединяем их с <br>

		    document.getElementById('output').innerHTML = firstTwoLines; // Выводим результат на страницу
		})
		.catch(error => {
		    console.error('Ошибка:', error);
		    document.getElementById('output').innerHTML = 'Ошибка при загрузке файла';
		});
	});
}
