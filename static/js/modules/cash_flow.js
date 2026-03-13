import { field_is_empty, invalid_field, remove_isInvalid_class, is_NaN } from '../utils/validations.js'

// ELEMENTOS PARA MANIPULAR
const form_incomes = document.getElementById('form-incomes')
const form_expenses = document.getElementById('form-expenses')


// EVENTOS
// addEventListener -> precisa receber uma função, não o resultado dela
// Form de entradas
form_incomes.addEventListener('submit', async function (event) {
  event.preventDefault()

  const amount = form_incomes.querySelector('#amount')
  const date = form_incomes.querySelector('#date')
  const select_ctgs = form_incomes.querySelector('#select-ctgs')

  if (await check_form_budgets(amount, date, select_ctgs)) {
    form_incomes.submit()
  }
})

// Form de saídas
form_expenses.addEventListener('submit', async function (event) {
  event.preventDefault()

  const amount = form_expenses.querySelector('#amount')
  const date = form_expenses.querySelector('#date')
  const select_ctgs = form_expenses.querySelector('#select-ctgs')

  if (await check_form_budgets(amount, date, select_ctgs)) {
    form_expenses.submit()
  }

})


// FUNÇÕES
async function check_form_budgets(amount, date, select_ctgs) {

  let is_valid = true

  if (field_is_empty(amount)) {
    is_valid = invalid_field(amount, 'Valor obrigatório')
  }

  else if (is_NaN(amount)) {
    is_valid = invalid_field(amount, 'O valor deve ser um número')
  }

  else if (equals_0(amount)) {
    is_valid = invalid_field(amount, 'O valor deve ser maior que 0')
  }

  else if (amount.parentElement.parentElement.parentElement.parentElement.id === 'form-expenses') {
    if (await expenses_are_greater_than_total_cash(amount)) {
      is_valid = invalid_field(amount, 'Saldo indisponível')
    }
  }

  else {
    remove_isInvalid_class(amount)
  }

  if (field_is_empty(date)) {
    is_valid = invalid_field(date, 'Data obrigatória')
  } else {
    remove_isInvalid_class(date)
  }

  if (field_is_empty(select_ctgs)) {
    is_valid = invalid_field(select_ctgs, 'Categoria obrigatória')
  } else {
    remove_isInvalid_class(select_ctgs)
  }

  return is_valid
}

async function expenses_are_greater_than_total_cash(amount) {

  try {

    const amount_value = amount.value
    const res = await fetch('/expenses_are_greater_than_total_cash', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        amount: amount_value
      })
    })

    const data = await res.json()

    if (data.success) {
      return true
    } else {
      return false
    }

  } catch (error) {
    alert(`Ocorreu um erro no servidor: ${error}`)
  }

}

function equals_0(input) {
  const value = input.value
  const value_float = parseFloat(value)
  if (value_float == 0) {
    return true
  } else {
    return false
  }
}