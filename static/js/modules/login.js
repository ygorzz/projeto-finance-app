import { field_is_empty, invalid_field, remove_isInvalid_class, length_is_invalid, username_already_exists, contains_number, contains_char }
    from '../utils/validations.js'

// ELEMENTOS PARA MANIPULAR
const form = document.getElementById('form-login')


// EVENTOS
form.addEventListener('submit', async function (event) {
    event.preventDefault()

    let is_valid = true
    const username = form.querySelector('#username')
    const password = form.querySelector('#password')

    if (field_is_empty(username)) {
        is_valid = invalid_field(username, 'Nome de usuário obrigatório')

    }

    else if (length_is_invalid(username)) {
        is_valid = invalid_field(username, 'Usuário ou senha inválidos')

    }

    else {
        remove_isInvalid_class(username)
    }

    if (field_is_empty(password)) {
        is_valid = invalid_field(password, 'Senha obrigatória')
    }

    else if (length_is_invalid(password) || !contains_number(password) || !contains_char(password)) {

        is_valid = invalid_field(password, 'Usuário ou senha inválidos')
    }

    else{
        remove_isInvalid_class(password)
    }

    if(is_valid){
        if (!(await user_is_registered(username, password))) {
            is_valid = invalid_field(password, 'Usuário ou senha inválidos')
            invalid_field(username, 'Usuário ou senha inválidos')
        }
    }

    // Se for válido(não houver nenhum erro nos campos) o form é enviado
    if (is_valid) {
        form.submit()
    }
})


// FUNÇÕES //
async function user_is_registered(username, password) {

    try {

        const user_value = username.value
        const pass_value = password.value
        // encodeURIComponent - decodifica alguns caracteres
        const res = await fetch('/check_user_is_registered', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: user_value,
                password: pass_value
            })
        })
        const data = await res.json()

        // success = true -> usuário já esta registrado
        if (data.success) {
            return true
        } else {
            return false
        }

    } catch (error) {
        alert(`Houve um erro no servidor: ${error}`)
    }
}