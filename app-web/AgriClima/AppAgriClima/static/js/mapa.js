var map = L.map('map').setView([-15.0830, -44.1600], 9);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var estacoesData = [];
var clickMarker; // Variável global para armazenar o marcador de clique
var markers = []; // Array para armazenar todos os marcadores de estações
var isUpdatingNearestStations = false;
var isUpdatingMap = false;
var isMapMoving = false;



// Função para adicionar marcadores ao mapa
function addMarkers(estacoes) {
    estacoesData = estacoes;
    
    estacoes.forEach(function(estacao) {
        var nome = estacao.nome;
        var codigo = estacao.codigo;
        var latitude = parseFloat(estacao.latitude);
        var longitude = parseFloat(estacao.longitude);
        var tipoEstacao = estacao.tipoEstacao;
        var fonte = estacao.fonte;

        var fillColor = fonte === 'INMET' ? '#FFDB00' : '#0053AB';

        // Construir o conteúdo do popup
        var popupContent = `
            <b>Nome:</b> ${nome}<br>
            <b>Código:</b> ${codigo}<br>
            <b>Tipo de Estação:</b> ${tipoEstacao}<br>
            <b>Fonte:</b> ${fonte} <br>
            <b>Coordenadas:</b> ${latitude}, ${longitude}<br>
        `;

        // Adicionar o marcador como um círculo com cor base no tipo de estação
        var marker = L.circleMarker([latitude, longitude], {
            radius: 5,
            color: 'white',
            weight: 1,
            fillColor: fillColor,
            fillOpacity: 1
        }).addTo(map).bindPopup(popupContent);
        
        // Adicionar um evento de clique ao marcador para preencher o formulário com o nome da estação
        marker.on('click', function() {
            document.getElementById('nome-estacao').value = this.options.popupContent;
            document.getElementById('cod-estacao').value = this.options.codigo;
        });

        // Define propriedades personalizadas para acessar dentro do evento de clique
        marker.options.popupContent = nome;
        marker.options.codigo = codigo;

        // Adiciona o marcador ao array de marcadores
        markers.push(marker);
    });
}

// Função para carregar marcadores de forma assíncrona
function loadMarkersAsync() {
    if (isUpdatingMap) return;

    // Faz uma solicitação ao servidor para obter os dados das estações
    fetch('/get_estacoes/')
        .then(response => response.json())
        .then(estacoes => addMarkers(estacoes))
        .catch(error => console.error('Erro:', error));
}


// Função para carregar marcadores quando o mapa termina de mover
function onMapMoveEnd() {
    if (isMapMoving) {
        var lat = parseFloat(document.getElementById('latitude').value);
        var lng = parseFloat(document.getElementById('longitude').value);

        // Remove marcador anterior, se existir
        if (clickMarker) {
            map.removeLayer(clickMarker);
        }

        // Adiciona novo marcador na posição especificada
        clickMarker = L.marker([lat, lng]).addTo(map);

        // Atualiza as estações próximas
        updateNearestStations(lat, lng);

        isMapMoving = false;
    }
}

// Adiciona um evento de movimento de mapa para carregar marcadores assincronamente
map.on('moveend', onMapMoveEnd);

// Carrega marcadores iniciais
loadMarkersAsync();

// ===============================================================================

// Função para calcular a distância entre duas coordenadas usando a fórmula de Haversine
function getDistance(lat1, lon1, lat2, lon2) {
    var R = 6371; // Raio da Terra em km
    var dLat = (lat2 - lat1) * Math.PI / 180;
    var dLon = (lon2 - lon1) * Math.PI / 180;
    var a = 
        0.5 - Math.cos(dLat)/2 + 
        Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
        (1 - Math.cos(dLon)) / 2;
    return R * 2 * Math.asin(Math.sqrt(a));
}

// Função para atualizar as cores dos marcadores com base na proximidade ao ponto especificado
function updateNearestStations(lat, lng) {
    isUpdatingMap = true;
    map.off('moveend', onMapMoveEnd);

    var nearestStations = estacoesData.map(function(estacao) {
        estacao.distance = getDistance(lat, lng, estacao.latitude, estacao.longitude);
        return estacao;
    }).sort(function(a, b) {
        return a.distance - b.distance;
    }).slice(0, 10); // Seleciona as 10 estações mais próximas

    // Atualiza a cor dos marcadores
    markers.forEach(function(marker) {
        var estacao = nearestStations.find(est => est.codigo === marker.options.codigo);
        if (estacao) {
            marker.setStyle({ fillColor: '#E53E30' });
        } else {
            var estacaoOriginal = estacoesData.find(est => est.codigo === marker.options.codigo);
            var fillColor = estacaoOriginal.fonte === 'INMET' ? '#FFDB00' : '#0053AB';
            marker.setStyle({ fillColor: fillColor });
        }
    });

    map.on('moveend', onMapMoveEnd);
    isUpdatingMap = false;
}



// Adiciona um evento de clique no mapa para preencher latitude e longitude
map.on('click', function(e) {
    if (document.getElementById('mode2-btn').classList.contains('active')) {
        // Remove marcador anterior, se existir
        if (clickMarker) {
            map.removeLayer(clickMarker);
        }

        // Adiciona novo marcador no ponto clicado
        clickMarker = L.marker(e.latlng).addTo(map);

        // Preenche os campos de latitude e longitude no formulário
        document.getElementById('latitude').value = e.latlng.lat;
        document.getElementById('longitude').value = e.latlng.lng;

        // Atualiza as estações próximas
        updateNearestStations(e.latlng.lat, e.latlng.lng);
    }
});


// Função para alternar entre os modos de busca
function setSearchMode(mode) {
    const description = document.getElementById('description');
    if (mode === 1) {
        document.getElementById('form1').style.display = 'block';
        document.getElementById('form2').style.display = 'none';
        document.getElementById('mode1-btn').classList.add('active');
        document.getElementById('mode2-btn').classList.remove('active');
        description.innerText = 'Selecione uma estação no mapa abaixo para fazer download';
    } else if (mode === 2) {
        document.getElementById('form1').style.display = 'none';
        document.getElementById('form2').style.display = 'block';
        document.getElementById('mode1-btn').classList.remove('active');
        document.getElementById('mode2-btn').classList.add('active');
        description.innerText = 'Selecione um local no mapa ou preencha as coordenadas para listar estações próximas';
    }
}

// Função para encontrar as estações mais próximas e exibi-las no modal
function findNearestStations(event) {
    event.preventDefault();

    var lat = parseFloat(document.getElementById('latitude').value);
    var lng = parseFloat(document.getElementById('longitude').value);

    // Verifica se ambos os campos de latitude e longitude estão preenchidos
    if (isNaN(lat) || isNaN(lng)) {
        alert('Por favor, preencha as coordenadas de latitude e longitude.');
        return;
    }

    // Adiciona a distância ao objeto de estação
    var estacoesComDistancia = estacoesData.map(function(estacao) {
        estacao.distance = getDistance(lat, lng, estacao.latitude, estacao.longitude);
        return estacao;
    });

    // Ordena as estações pela distância
    estacoesComDistancia.sort(function(a, b) {
        return a.distance - b.distance;
    });

    // Seleciona as 10 estações mais próximas
    var nearestStations = estacoesComDistancia.slice(0, 10);

    // Exibe as estações em uma tabela no modal
    var tableBody = document.querySelector('#nearest-stations-table tbody');
    tableBody.innerHTML = '';
    nearestStations.forEach(function(estacao) {
        var row = document.createElement('tr');
        row.innerHTML = `
            <td><input type="checkbox" class="station-checkbox" data-nome="${estacao.nome}" data-codigo="${estacao.codigo}" data-fonte="${estacao.fonte}" data-latitude="${estacao.latitude}" data-longitude="${estacao.longitude}"></td>
            <td>${estacao.nome}</td>
            <td>${estacao.codigo}</td>
            <td>${estacao.fonte}</td>
            <td>${estacao.latitude}</td>
            <td>${estacao.longitude}</td>
        `;
        tableBody.appendChild(row);
    });

    // Exibe o modal
    document.getElementById('nearest-stations-modal').style.display = 'block';

    // Adiciona o evento de selecionar todos
    var selectAllCheckbox = document.getElementById('select-all-checkbox');
    selectAllCheckbox.addEventListener('change', function() {
        var checkboxes = document.querySelectorAll('.station-checkbox');
        checkboxes.forEach(function(checkbox) {
            checkbox.checked = selectAllCheckbox.checked;
        });
    });

    // Atualiza as estações próximas no mapa
    updateNearestStations(lat, lng);
}

// Função para fechar o modal
function closeModal() {
    document.getElementById('nearest-stations-modal').style.display = 'none';
}

// ===============================================================================

// Adiciona um evento de mudança nos campos de latitude e longitude
function onCoordinateChange() {
    var lat = parseFloat(document.getElementById('latitude').value);
    var lng = parseFloat(document.getElementById('longitude').value);

    // Verifica se ambos os campos de latitude e longitude estão preenchidos
    if (!isNaN(lat) && !isNaN(lng)) {
        isMapMoving = true;
        map.setView([lat, lng], 9); // Ajusta o zoom e centra o mapa na nova posição
    }
}

// Adiciona eventos de mudança nos campos de latitude e longitude
document.getElementById('latitude').addEventListener('change', onCoordinateChange);
document.getElementById('longitude').addEventListener('change', onCoordinateChange);

// Adiciona o evento de "moveend" ao mapa
map.on('moveend', onMapMoveEnd);


// Adiciona evento ao botão de buscar para abrir o modal com as estações mais próximas
document.getElementById('search-button').addEventListener('click', findNearestStations);
