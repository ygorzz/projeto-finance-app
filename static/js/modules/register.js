import { field_is_empty, invalid_field, length_is_invalid, username_already_exists, email_is_invalid, remove_isInvalid_class, contains_char, contains_number, confirmation_is_valid, contains_only_alnum} from '../utils/validations.js'

// VARIÁVEIS AUXILIARES
const MAX_USERNAME = 20
const MIN_USERNAME = 4
const MAX_PASSWORD = 24
const MIN_PASSWORD = 8


// ELEMENTOS PARA MANIPULAR
const form = document.getElementById('form-register')


// EVENTOS
form.addEventListener('submit', async function (event) {
    event.preventDefault()

    let is_valid = true
    const username = form.querySelector('#username')
    const email = form.querySelector('#email')
    const password = form.querySelector('#password')
    const confirmation = form.querySelector('#confirmation')

    if (field_is_empty(username)) {
        is_valid = invalid_field(username, 'Nome de usuário obrigatório')
    }

    else if (length_is_invalid(username)) {
        is_valid = invalid_field(username, `Nome de usuário deve conter entre ${MIN_USERNAME} e ${MAX_USERNAME} caracteres`)

    }

    else if(!contains_only_alnum(username)){
        is_valid = invalid_field(username, 'Nome de usuário deve conter apenas letras e números')
    }

    else if (await username_already_exists(username)) {
        is_valid = invalid_field(username, 'Esse nome de usuário já existe')
    }

    else {
        remove_isInvalid_class(username)
    }

    if (field_is_empty(email)) {
        is_valid = invalid_field(email, 'Email obrigatório')

    }

    else if (email_is_invalid(email)) {
        is_valid = invalid_field(email, 'Formato de email inválido')

    }

    else if (await email_already_exists(email)) {
        is_valid = invalid_field(email, 'Esse email já está registrado')
    }

    else {
        remove_isInvalid_class(email)
    }

    if (field_is_empty(password)) {
        is_valid = invalid_field(password, 'Senha obrigatória')
    }

    else if (length_is_invalid(password)) {
        is_valid = invalid_field(password, `Senha deve conter entre ${MIN_PASSWORD} e ${MAX_PASSWORD} caracteres`)
    }

    else if (!contains_number(password)) {
        is_valid = invalid_field(password, 'Senha deve conter ao menos um número')
    }

    else if (!contains_char(password)) {
        is_valid = invalid_field(password, 'Senha deve conter ao menos uma letra')
    }

    else {
        remove_isInvalid_class(password)
    }

    if (field_is_empty(confirmation)) {
        is_valid = invalid_field(confirmation, 'Confirmação obrigatória')
    }

    else if (!confirmation_is_valid(confirmation, password)) {
        is_valid = invalid_field(confirmation, 'Confirmação inválida')
    }

    else {
        remove_isInvalid_class(confirmation)
    }

    // Se for válido(não houver nenhum erro nos campos) o form é enviado
    if (is_valid) {
        form.submit()
    }
})


// FUNÇÕES
async function email_already_exists(input) {

    try {
        const email_value = input.value
        const res = await fetch('/check_email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email_value
            })
        })
        const data = await res.json()

        // success = true -> email já existe
        if (data.success) {
            return true
        } else {
            return false
        }
    } catch (error) {
        alert(`Houve um erro no servidor: ${error}`)
    }
}

