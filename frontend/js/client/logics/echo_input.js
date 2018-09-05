let input = document.querySelector('#input')
let reply = document.querySelector('#reply')

input.addEventListener('input', () => {
  client.invoke("echo", input.value, (error, rep) => {
    if(error) {
      console.error(error)
    } else {
      reply.textContent = rep
    }
  })
})

input.dispatchEvent(new Event('input'))