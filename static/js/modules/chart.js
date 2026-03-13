// Gráfico view Dashboard via CDN

// Função para criar o gráfico
async function create_char(){

  // ELEMENTOS PARA MANIPULAR
  const ctx = document.getElementById('meu-grafico')
  const div_error = document.getElementById('message')

  // Se o elemento existe
  if (ctx){

    const items = await get_spent_by_category()
    
    if(!items == ""){
      const labels = items.map(item => item.name)
      const data = items.map(item => item.total_amount)
      new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            label: 'R$',
            data: data,
            borderWidth: 3
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      })
    }else{
      div_error.innerHTML = '<p>Ainda não há gastos em categorias'
    }

  }

}

// Chamada da função
create_char()

async function get_spent_by_category(){

  // Captura os parâmetros que já estão na URL do navegador
  const params = new URLSearchParams(window.location.search);
  const month = params.get('select-month') || "";
  const year = params.get('select-year') || "";

  const res = await fetch(`/get_spent_by_category?month=${month}&year=${year}`)
  const data = await res.json()
  
  if(data.datas === 'empty'){
    return ""
  }else{
    return data.datas
  }
}
