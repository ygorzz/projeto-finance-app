// ELEMENTOS PARA MANIPULAR
const btns_delete = document.querySelectorAll('#btn-delete')


// EVENTOS
btns_delete.forEach(btn => {
    btn.addEventListener('click', delete_transaction)
})


// FUNÇÕES
async function delete_transaction(event){
    const btn = event.currentTarget
    const id = btn.dataset.id
    const res = await fetch(`/delete_transaction/${id}`, {
        method: "DELETE"
    })

    if(res.ok){
        btn.closest('.delete-by-js').remove()
        // Redireciona para a mesma rota. Dessa forma, quando não houver nenhuma categoria, a mensagem de aviso é exibida logo após a exclusão
        window.location.href = '/history'
    }
}