function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');






const btnsAdicionar = document.querySelectorAll(".adicionar-item");

btnsAdicionar.forEach(btn => {
    btn.addEventListener("click", adicionarAoCarrinho)
})

function adicionarAoCarrinho(e) {
    let product_id = e.target.value
    let url = "/carrinho/adicionar"

    let dados = { id: product_id }

    fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json", 'X-CSRFToken': csrftoken },
        body: JSON.stringify(dados)
    })
        .then(res => res.json())
        .then(data => {
            document.getElementById("itens_carrinho").innerHTML = data
            console.log(data)
        })
        .catch(error => {
            console.log(error)
        })
}

const btnsRemover = document.querySelectorAll(".remover-item");

btnsRemover.forEach(btn => {
    btn.addEventListener("click", removerDoCarrinho)
})

function removerDoCarrinho(e) {
    let product_id = e.target.value
    let url = "/carrinho/remover"

    let dados = { id: product_id }

    fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json", 'X-CSRFToken': csrftoken },
        body: JSON.stringify(dados)
    })
        .then(res => res.json())
        .then(data => {
            document.getElementById("itens_carrinho").innerHTML = data
            console.log(data)
        })
        .catch(error => {
            console.log(error)
        })
}