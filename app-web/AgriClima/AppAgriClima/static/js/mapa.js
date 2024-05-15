var map = L.map('map').setView([-15.0830, -44.1600], 9);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Função para adicionar marcadores ao mapa
function addMarkers(estacoes) {
    estacoes.forEach(function(estacao) {
        var nome = estacao.nome;
        var codigo = estacao.codigo;
        var latitude = parseFloat(estacao.latitude);
        var longitude = parseFloat(estacao.longitude);
        var tipoEstacao = estacao.tipoEstacao;
        var fonte = estacao.fonte;

        var fillColor = fonte === 'INMET' ? 'yellow' : 'blue';

        // Construir o conteúdo do popup
        var popupContent = `
            <b>Nome:</b> ${nome}<br>
            <b>Código:</b> ${codigo}<br>
            <b>Tipo de Estação:</b> ${tipoEstacao}<br>
            <b>Fonte:</b> ${fonte}
        `;

        // Adicionar o marcador como um círculo com cor base no tipo de estação
        var marker = L.circleMarker([latitude, longitude], {
            radius: 5,
            color: 'white',
            weight: 2,
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
    });
}

// Função para carregar marcadores de forma assíncrona
function loadMarkersAsync() {
    // Faz uma solicitação ao servidor para obter os dados das estações
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
