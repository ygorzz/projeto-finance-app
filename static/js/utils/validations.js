const MAX_USERNAME = 20
const MIN_USERNAME = 4
const MAX_PASSWORD = 24
const MIN_PASSWORD = 8

export async function username_already_exists(input) {

    try {
        const user_value = input.value
        // encodeURIComponent -> estamos passando valores pela url (GET) e ela não interpretará corretamente alguns caracteres por padrão(ex: @)
        // logo usamos essa função para que o servidor decodifique corretamente o caractere
        const req = await fetch('/check_username', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: user_value
            })
        })
        const data = await req.json()

        // success = true -> usuário já existe
        if (data.success) {
            return true
        } else {
            return false
        }
    } catch (error) {
        alert(`Houve um erro no servidor: ${error}`)
    }
}

export function field_is_empty(field) {
    let is_empty = false
    if (field.value.trim() === '') {
        is_empty = true
    }

    return is_empty
}

export function length_is_invalid(input) {

    let is_invalid = false

    let max_length
    let min_length

    if (input.id === 'username') {
        max_length = MAX_USERNAME
        min_length = MIN_USERNAME

        if (input.value.length > max_length || input.value.length < min_length) {
            is_invalid = true
        }
    }

    else if (input.id === 'password') {
        max_length = MAX_PASSWORD
        min_length = MIN_PASSWORD

        if (input.value.length > max_length || input.value.length < min_length) {
            is_invalid = true
        }
    }

    return is_invalid
}

export function invalid_field(field, message) {
    // Acessa a div que exibe as mensagens de erro
    const message_error = field.parentElement.querySelector('.invalid-feedback')
    field.classList.add('is-invalid')
    message_error.textContent = message
    return false
}

export function email_is_invalid(input) {

    let is_invalid = false

    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

    if (!regex.test(input.value)) {
        is_invalid = true
    }

    return is_invalid
}

export function contains_number(input) {

    // Expressão regular para verificar se existe um dígito
    const regex = /\d/

    if (regex.test(input.value)) {
        return true
    }

    return false
}

export function contains_char(input) {

    // Expressão regular para verificar se existe alguma letra
    const regex = /[a-zA-Z]/

    if (regex.test(input.value)) {
        return true
    }

    return false
}

export function contains_only_alnum(input){

    // testa se há apenas letras e números
    const regex = /^[a-zA-Z0-9]+$/

    if(regex.test(input.value)){
        return true
    }else{
        return false
    }
}

export function confirmation_is_valid(confirmation, password) {

    if (confirmation.value !== password.value) {
        return false
    }
    return true
}

// Retorna true se for NaN
export function is_NaN(input) {
    let value = input.value.trim().replace(',', '.')
    let number = Number(value)

    if (Number.isNaN(number)) {
        return true
    }

    return false
}

export function remove_isInvalid_class(input) {
    input.classList.remove('is-invalid')
}