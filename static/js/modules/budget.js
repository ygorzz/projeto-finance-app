import { field_is_empty, invalid_field, remove_isInvalid_class, is_NaN } from '../utils/validations.js'

// ELEMENTOS PARA MANIPULAR
const form = document.getElementById('form-budget')
const btns_delete = document.querySelectorAll('#btn-delete')
const btn_cancel = document.getElementById('btn-cancel')


// EVENTOS
btn_cancel.addEventListener('click', () => {
    form.querySelector('#select-ctgs').value = ""
    form.querySelector('#amount').value = ""
})

btns_delete.forEach(btn => {
    btn.addEventListener('click', delete_budget)
})

form.addEventListener('submit', function (event) {
    event.preventDefault()

    let is_valid = true

    const select_ctgs = form.querySelector('#select-ctgs')
    const amount = form.querySelector('#amount')

    if (field_is_empty(select_ctgs)) {
        is_valid = invalid_field(select_ctgs, 'Categoria obrigatória')
    } else {
        remove_isInvalid_class(select_ctgs)
    }

    if (field_is_empty(amount)) {
        is_valid = invalid_field(amount, 'Valor obrigatório')
    }

    else if (is_NaN(amount)) {
        is_valid = invalid_field(amount, 'O valor deve ser um número')
    }
    else {
        remove_isInvalid_class(amount)
    }

    // Se for válido(não houver nenhum erro nos campos) o form é enviado
    if(is_valid){
        form.submit()
    }
})


// FUNÇOES
async function delete_budget(event){
    
    const btn = event.currentTarget // armazena o elemento clicado
    const id = btn.dataset.id // armazena o valor do atributo data-id
    const res = await fetch(`/delete_budget/${id}`, {
        method: "DELETE"
    })

    if(res.ok){
        btn.closest('.card').remove()
        // Redireciona para a mesma rota. Dessa forma, quando não houver nenhuma categoria, a mensagem de aviso é exibida logo apóa a exclusão 
        window.location.href = '/budget'
    }
    
}