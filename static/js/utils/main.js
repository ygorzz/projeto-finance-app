// Evento para limpar mensagens de erros nos forms
// Ao clicar no html
document.addEventListener('click', function(event){

    const inputs_invalids = document.querySelectorAll('.is-invalid')
    const cards = document.querySelectorAll('.card')

    let clicked_on_the_card = false

    // Se o card contém o elemento clicado - 'se clicou no card'
    cards.forEach(card => {
        if(card.contains(event.target)){
            clicked_on_the_card = true
        }
    })

    // Se não clicou no card, limpa as menssagens
    if(!clicked_on_the_card){
        inputs_invalids.forEach(input => {
            input.classList.remove('is-invalid')    
        })
    }
})