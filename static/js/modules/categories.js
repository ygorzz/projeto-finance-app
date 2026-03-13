import { field_is_empty, invalid_field, remove_isInvalid_class } from '../utils/validations.js'

// ELEMENTOS PARA MANIPULAR
const form = document.getElementById('form-ctgs')
const btns_delete = document.querySelectorAll('#btn-delete')
const btn_cancel = document.getElementById('btn-cancel')


// EVENTOS
btn_cancel.addEventListener('click', () => {
    form.querySelector('#ctg-name').value = ""
})

btns_delete.forEach(btn =>{
    btn.addEventListener('click', delete_category)
})

form.addEventListener('submit', async function (event) {
    event.preventDefault()

    let is_valid = true
    const name_ctg = form.querySelector('#ctg-name')
    
    if (field_is_empty(name_ctg)) {
        is_valid = invalid_field(name_ctg, 'Nome obrigatório')
    }

    else if (await category_already_exists(name_ctg)) {
        is_valid = invalid_field(name_ctg, 'Essa categoria já existe')
    }

    else {
        remove_isInvalid_class(name_ctg)
    }
    
    // Se for válido(não houver nenhum erro nos campos) o form é enviado
    if (is_valid) {
        form.submit()
    }
})


// FUNÇÕES
async function category_already_exists(name_ctg) {

    try {
        const category_value = name_ctg.value
        const res = await fetch('/check_category', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                category: category_value
            })
        })
        const data = await res.json()

        // success = true -> categoria ja existe
        if (data.success) {
            return true
        } else {
            return false
        }
    } catch (error) {
        alert(`Houve um erro no servidor: ${error}`)
    }
}

async function delete_category(event){
    const btn = event.currentTarget
    // dataset -> pega o atributo data-alguma_coisa
    const id = btn.dataset.id
    const res = await fetch(`/delete_category/${id}`, {
        method: "DELETE"
    })

    // Se a requisição foi bem sucedida
    if(res.ok){
        //closest -> pega o elemento container que possui o parâmetro
        btn.closest('.card').remove()
        // Redireciona para a mesma rota. Dessa forma, quando não houver nenhuma categoria, a mensagem de aviso é exibida logo após a exclusão
        window.location.href = '/categories'
    }
}
