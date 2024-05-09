var map = L.map('map').setView([-15.0830, -44.1600], 9);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// // Adiciona um evento de clique ao mapa para obter o nome da estação
// map.on('click', function(e) {
//     var latlng = e.latlng;
//     var latitude = latlng.lat.toFixed(6);
//     var longitude = latlng.lng.toFixed(6);

//     // Faz uma solicitação ao servidor para obter o nome da estação com base nas coordenadas
//     fetch(`/get_nome_estacao/?latitude=${latitude}&longitude=${longitude}`)
//         .then(response => response.json())
//         .then(data => {
//             if (data.nomeEstacao) {
//                 // Define o valor do campo de input 'municipio' como o nome da estação
//                 document.getElementById('municipio').value = data.nomeEstacao;
//             } else {
//                 // Se nenhuma estação for encontrada, limpa o valor do campo de input 'municipio'
//                 document.getElementById('municipio').value = '';
//             }
//         })
//         .catch(error => console.error('Erro:', error));
// });


// Função para adicionar marcadores ao mapa
function addMarkers(estacoes) {
    estacoes.forEach(function(estacao) {
        var nome = estacao.nome;
        var codigo = estacao.codigo;
        var latitude = parseFloat(estacao.latitude);
        var longitude = parseFloat(estacao.longitude);
        var tipoEstacao = estacao.tipoEstacao;

        var fillColor = tipoEstacao === '1' ? 'yellow' : 'blue';

        // Adicionar o marcador como um círculo com cor base no tipo de estação
        var marker = L.circleMarker([latitude, longitude], {
            radius: 5,
            color: 'white',
            weight: 2,
            fillColor: fillColor,
            fillOpacity: 1
        }).addTo(map).bindPopup(nome);
        
        // Adicionar um evento de clique ao marcador para preencher o formulário com o nome da estação
        marker.on('click', function() {
            document.getElementById('nome-estacao').value = this.options.popupContent;
            document.getElementById('cod-estacao').value = this.options.codigo;
        });

        // Define propriedades personalizadas para acessar dentro do evento de clique
        marker.options.popupContent = nome;
        marker.options.codigo = codigo;
    });
    

    // Armazena os dados dos marcadores no cache do navegador para uso futuro
    localStorage.setItem('cachedMarkers', JSON.stringify(estacoes));
}



// Função para carregar marcadores de forma assíncrona
function loadMarkersAsync() {
    // Verifica se os dados estão armazenados no cache do navegador
    var cachedMarkers = localStorage.getItem('cachedMarkers');
    
    if (cachedMarkers) {
        // Se os dados estiverem no cache, adiciona os marcadores diretamente do cache
        addMarkers(JSON.parse(cachedMarkers));
        
    } else {
        // Se os dados não estiverem no cache, faz uma solicitação ao servidor
        
        fetch('/get_estacoes/')
            .then(response => response.json())
            .then(estacoes => addMarkers(estacoes))
            .catch(error => console.error('Erro:', error));

        
    }
}

// Função para carregar marcadores quando o mapa termina de mover
function onMapMoveEnd() {
    loadMarkersAsync();
}

// Adiciona um evento de movimento de mapa para carregar marcadores assincronamente
map.on('moveend', onMapMoveEnd);

// Carrega marcadores iniciais
loadMarkersAsync();
