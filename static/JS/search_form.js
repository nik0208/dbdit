const idOsInput = document.getElementById('id_os_input');
const idOsResults = document.getElementById('id_os_results');

idOsInput.addEventListener('input', function() {
    const searchTerm = idOsInput.value;
    if (searchTerm.length >= 3) {
        fetch(`/search-os/?search_term=${searchTerm}`)
            .then(response => response.json())
            .then(data => {
                idOsResults.innerHTML = '';
                data.forEach(result => {
                    const resultItem = document.createElement('div');
                    resultItem.textContent = result.id_os;
                    idOsResults.appendChild(resultItem);
                });
            });
    } else {
        idOsResults.innerHTML = '';
    }
});