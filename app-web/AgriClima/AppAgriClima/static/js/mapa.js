var map = L.map('map').setView([-15.0830, -44.1600], 9);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Adiciona um evento de clique ao mapa para obter o nome do município
map.on('click', function(e) {
    var latlng = e.latlng;
    var latitude = latlng.lat.toFixed(6);
    var longitude = latlng.lng.toFixed(6);

    // Requisição para o serviço de geocodificação Nominatim para obter o nome do município
    var url = 'https://nominatim.openstreetmap.org/reverse?format=json&lat=' + latitude + '&lon=' + longitude + '&zoom=18&addressdetails=1';
    fetch(url)
        .then(response => response.json())
        .then(data => {
            var municipio = data.address.city || data.address.town || data.address.village || data.address.municipality;
            document.getElementById('municipio').value = municipio;
        })
        .catch(error => console.error('Erro:', error));
});

// Adiciona um evento de mouseover e mouseout para os marcadores do mapa
map.on('mouseover', function(e) {
    var layer = e.layer;

    if (layer instanceof L.Marker) {
        layer._icon.style.cursor = 'pointer'; // Altera o cursor para pointer ao passar sobre o marcador
        layer._icon.style.color = '#007bff'; // Altera a cor do texto para azul ao passar sobre o marcador
    }
});

map.on('mouseout', function(e) {
    var layer = e.layer;

    if (layer instanceof L.Marker) {
        layer._icon.style.cursor = 'default'; // Restaura o cursor para o padrão
        layer._icon.style.color = '#000'; // Restaura a cor do texto para preto
    }
});

// Função para adicionar marcadores ao mapa
function addMarkers(estacoes) {
    estacoes.forEach(function(estacao) {
        var nome = estacao.nome;
        var latitude = parseFloat(estacao.latitude);
        var longitude = parseFloat(estacao.longitude);
        L.marker([latitude, longitude]).addTo(map).bindPopup(nome);
    });
}

// Função para carregar marcadores de forma assíncrona
function loadMarkersAsync() {
    fetch('/get_estacoes/')
        .then(response => response.json())
        .then(estacoes => addMarkers(estacoes))
        .catch(error => console.error('Erro:', error));
}

// Função para carregar marcadores quando o mapa termina de mover
function onMapMoveEnd() {
    loadMarkersAsync();
}

// Adiciona um evento de movimento de mapa para carregar marcadores assincronamente
map.on('moveend', onMapMoveEnd);

// Carrega marcadores iniciais
loadMarkersAsync();
