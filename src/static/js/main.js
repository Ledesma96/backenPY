const socket = io()
const btn = document.getElementById('btn')
const form = document.getElementById('form')
const send = document.getElementById('send')
const tbody = document.getElementById('tbody')



btn.addEventListener('click', function(){

    if(form.classList.contains('close')) {
        form.classList.remove('close')
        form.classList.add('open')
    }
})

const closeForm = () => {
    if(form.classList.contains('open')){
        form.classList.remove('open')
        form.classList.add('close')
    } 
}



send.addEventListener('click', function(){
     const title = document.getElementById('title').value;
     const gender = document.getElementById('gender').value;
     const year = document.getElementById('year').value;
     const price = document.getElementById('price').value;
     const ratings = document.getElementById('ratings').value;

     const film = {
         title: title,
         gender: gender,
         year: year,
         price: price,
         ratings: ratings
     }
     socket.emit('add-film', film)

     closeForm()

    //  fetch('/add-film', {
    //      method: 'POST',
    //      headers: {
    //          'Content-Type': 'application/json'
    //      },
    //      body: JSON.stringify(film)
    //  })
    //  .then(response => response.json())
    //  .then(data => console.log(data))
    //  .catch(err => console.error('Error:', err))
})

const deleteFilm = (id) => {
    socket.emit('remove-film', id)
}

socket.on('all-films', function(data){
    const films = JSON.parse(data);
    console.log(films);
    tbody.innerHTML =''
    films.data.forEach(film => {
        const row = `
                            <tr>
                                <td>${film.id}</td>
                                <td>${film.title}</td>
                                <td>${film.gender}</td>
                                <td>${film.year}</td>
                                <td>$${film.price.toFixed(2)}</td>
                                <td>${film.ratings}</td>
                                <td class='delete' onclick="deleteFilm('${film.id}')">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"/>
                                        <path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"/>
                                    </svg>
                                </td>
                            </tr>
                        `;
        tbody.innerHTML += row
    })
})